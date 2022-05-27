import fire
from .seeder import seed

if __name__ == '__main__':
    """CLI application for seeding the database."""
    fire.Fire(seed)
