"""
Setup script for Car Scout application
"""

import os
import subprocess
import sys

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    else:
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def setup_environment():
    """Set up environment file"""
    env_example = ".env.example"
    env_file = ".env"
    
    if not os.path.exists(env_file):
        if os.path.exists(env_example):
            print("📝 Creating .env file from template...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your actual values:")
            print("   - TELEGRAM_BOT_TOKEN (get from @BotFather)")
            print("   - Other configuration values as needed")
        else:
            print("❌ .env.example file not found")
    else:
        print("✅ .env file already exists")

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "data"
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")

def main():
    """Main setup function"""
    print("🚗 Car Scout Setup")
    print("=" * 50)
    
    check_python_version()
    install_dependencies()
    setup_environment()
    create_directories()
    
    print("\n" + "=" * 50)
    print("✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your bot token")
    print("2. Get bot token from @BotFather on Telegram:")
    print("   - Send /newbot to @BotFather")
    print("   - Choose a name and username for your bot")
    print("   - Copy the token to TELEGRAM_BOT_TOKEN in .env")
    print("3. Run: python main.py")
    print("\n🎯 Your bot will be ready to monitor car listings!")

if __name__ == "__main__":
    main()
