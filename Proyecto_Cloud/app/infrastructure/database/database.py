from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import asyncio
from app.infrastructure.config.config import settings
from app.infrastructure.database.models import Base

engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"auth_plugin": "mysql_native_password"}  # <- Especificar plugin de autenticación
)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def wait_for_db(max_retries: int = 20, delay: float = 3.0):
    """Esperar a que la base de datos esté disponible"""
    for i in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            print("✅ Base de datos conectada exitosamente")
            return
        except Exception as e:
            print(f"⌛ Intento {i+1}/{max_retries}: {str(e)[:100]}...")
            if i < max_retries - 1:
                await asyncio.sleep(delay)
    
    raise Exception(f"❌ No se pudo conectar a la base de datos después de {max_retries} intentos")

async def init_db():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas creadas exitosamente")
    except Exception as e:
        print(f"❌ Error creando tablas: {e}")
        raise