"""
Setup Script for Trading Application
Run this to set up everything automatically
"""
import subprocess
import sys
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def install_dependencies():
    """Install required packages"""
    print_header("📦 Installing Dependencies")
    
    try:
        print("Installing packages from requirements.txt...")
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            "requirements.txt"
        ])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_header("📁 Creating Directories")
    
    directories = [
        "data",
        "data/historical",
        "logs",
        "reports"
    ]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}/")
    
    print("✅ All directories created!")
    return True

def test_imports():
    """Test if all imports work"""
    print_header("🧪 Testing Imports")
    
    try:
        print("Testing pandas...")
        import pandas
        print("✅ pandas OK")
        
        print("Testing numpy...")
        import numpy
        print("✅ numpy OK")
        
        print("Testing yfinance...")
        import yfinance
        print("✅ yfinance OK")
        
        print("Testing matplotlib...")
        import matplotlib
        print("✅ matplotlib OK")
        
        print("\n✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_connection():
    """Test data fetching"""
    print_header("🔗 Testing Data Connection")
    
    try:
        from data.free_fetcher import FreeFetcher
        
        print("Creating data fetcher...")
        fetcher = FreeFetcher()
        
        print("Testing connection with RELIANCE...")
        quote = fetcher.get_quote('RELIANCE')
        
        if quote and quote['last_price'] > 0:
            print(f"✅ Connection successful!")
            print(f"   RELIANCE Price: ₹{quote['last_price']:.2f}")
            return True
        else:
            print("⚠️  Connection test inconclusive")
            return True  # Don't fail setup
    except Exception as e:
        print(f"⚠️  Connection test failed: {e}")
        print("   (This is OK - internet might be required)")
        return True  # Don't fail setup

def show_next_steps():
    """Show next steps to user"""
    print_header("🎉 Setup Complete!")
    
    print("\n✅ Your trading application is ready to use!")
    print("\n📚 Next Steps:\n")
    print("1. Read the Quick Start Guide:")
    print("   → Open QUICK_START.md")
    print("\n2. Run the application:")
    print("   → python main.py")
    print("\n3. Try the examples:")
    print("   → python example_usage.py")
    print("\n4. Read full documentation:")
    print("   → Open README.md")
    
    print("\n" + "="*60)
    print("  Ready to start trading! 🚀")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("  🚀 AUTOMATED TRADING APPLICATION")
    print("  Setup Script")
    print("="*60)
    print("\nThis will set up everything you need to get started.\n")
    
    input("Press Enter to continue...")
    
    # Step 1: Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed at dependency installation")
        return False
    
    # Step 2: Create directories
    if not create_directories():
        print("\n❌ Setup failed at directory creation")
        return False
    
    # Step 3: Test imports
    if not test_imports():
        print("\n❌ Setup failed at import testing")
        return False
    
    # Step 4: Test data connection (optional)
    test_data_connection()
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("✅ Setup completed successfully!")
            print("Run: python main.py\n")
        else:
            print("\n❌ Setup encountered issues. Check errors above.")
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

