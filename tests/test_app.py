from flask import request, jsonify
from functools import wraps
import time
import logging
import redis
from cachelib import SimpleCache

# Configurações
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 3600  # 1 hora
CACHE_TIMEOUT = 300  # 5 minutos

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inicialização do cache
try:
    cache = redis.Redis(host='localhost', port=6379, db=0)
except:
    logger.warning("Redis não disponível, usando cache em memória")
    cache = SimpleCache()

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        ip = request.remote_addr
        current = time.time()
        pipe = cache.pipeline()
        
        # Chave única para o IP
        key = f'rate_limit:{ip}'
        
        # Limpar requests antigos
        pipe.zremrangebyscore(key, 0, current - RATE_LIMIT_WINDOW)
        
        # Contar requests no período
        pipe.zcard(key)
        
        # Adicionar request atual
        pipe.zadd(key, {str(current): current})
        
        # Definir TTL
        pipe.expire(key, RATE_LIMIT_WINDOW)
        
        # Executar pipeline
        _, request_count, *_ = pipe.execute()
        
        if request_count > RATE_LIMIT_REQUESTS:
            logger.warning(f"Rate limit excedido para IP {ip}")
            return jsonify({'error': 'Rate limit exceeded'}), 429
            
        return f(*args, **kwargs)
    return decorated_function

def validate_file_size(file):
    if file.content_length > MAX_FILE_SIZE:
        logger.warning(f"Arquivo muito grande: {file.content_length} bytes")
        return False
    return True

def cache_response(timeout=CACHE_TIMEOUT):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Criar chave única baseada na requisição
            cache_key = f"cache:{request.path}:{hash(str(request.get_json()))}"
            
            # Tentar obter do cache
            rv = cache.get(cache_key)
            if rv is not None:
                logger.info(f"Cache hit para {cache_key}")
                return rv
                
            # Se não estiver no cache, executar função
            rv = f(*args, **kwargs)
            
            # Armazenar no cache
            cache.set(cache_key, rv, timeout=timeout)
            logger.info(f"Cache miss para {cache_key}")
            
            return rv
        return decorated_function
    return decorator