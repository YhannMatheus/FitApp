import asyncio
from tortoise import Tortoise
from datetime import datetime
from src.core.database.db_config import TORTOISE_ORM
from src.core.auth.security import Authenticate
from src.types.models.user import User
from src.types.enums.user import GenderEnum, ActivityLevelEnum

async def seed_database():
    """Seed do banco de dados com usuários de teste para login/registro"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

    print("🌱 Iniciando seed do banco de dados...")

    # Limpar usuários existentes
    await User.all().delete()

    # Criar Usuários de teste
    print("👤 Criando usuários de teste...")
    
    await User.create(
        email="john@example.com",
        name="John Doe",
        hashed_password=Authenticate.hash_password("password123"),
        birth_date=datetime(1990, 5, 15).date(),
        gender=GenderEnum.MALE,
        height_cm=175.0,
        activity_level=ActivityLevelEnum.MODERATELY_ACTIVE
    )

    await User.create(
        email="jane@example.com",
        name="Jane Smith",
        hashed_password=Authenticate.hash_password("password123"),
        birth_date=datetime(1995, 8, 20).date(),
        gender=GenderEnum.FEMALE,
        height_cm=165.0,
        activity_level=ActivityLevelEnum.VERY_ACTIVE
    )

    await User.create(
        email="admin@example.com",
        name="Admin User",
        hashed_password=Authenticate.hash_password("admin123"),
        birth_date=datetime(1985, 1, 1).date(),
        gender=GenderEnum.MALE,
        height_cm=180.0,
        activity_level=ActivityLevelEnum.MODERATELY_ACTIVE
    )

    print("✅ Seed concluído com sucesso!")
    print(f"   - {await User.all().count()} usuários criados")
    print("\n📧 Credenciais de teste:")
    print("   - john@example.com / password123")
    print("   - jane@example.com / password123")
    print("   - admin@example.com / admin123")

    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(seed_database())