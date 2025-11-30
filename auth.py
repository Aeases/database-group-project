from utils import getUserInput

class AuthSystem:
    def __init__(self):
        self.current_user = None
        self.current_level = None
    
    def login(self):
        print("\n=== CMMS Login ===")
        print("Choose your role:")
        print("1. Executive Officer")
        print("2. Mid-level Manager") 
        print("3. Base-level Worker")
        
        choice = getUserInput("Select role (1-3): ")
        
        if choice == "1":
            self.current_level = 'executive officer'
            self.current_user = "exec_officer"
            print("\nWelcome! You have executive-level access.")
        elif choice == "2":
            self.current_level = 'mid-level manager'
            self.current_user = "mid_manager"
            print("\nWelcome! You have manager-level access.")
        elif choice == "3":
            self.current_level = 'base-level worker'
            self.current_user = "base_worker"
            print("\nWelcome! You have worker-level access.")
        else:
            print("Invalid choice. Please select 1-3.")
            return False
            
        return True
    
    def logout(self):
        print(f"\nLogged out successfully. Thank you for using CMMS!")
        self.current_user = None
        self.current_level = None
    
    def has_permission(self, required_level):
        """Check if current user has required permission level"""
        if not self.current_user:
            return False
            
        level_hierarchy = {
            'base-level worker': 1,
            'mid-level manager': 2,
            'executive officer': 3
        }
        
        current_level_num = level_hierarchy.get(self.current_level, 0)
        required_level_num = level_hierarchy.get(required_level, 0)
        
        return current_level_num >= required_level_num
    
    def get_permission_level(self):
        return self.current_level

auth_system = AuthSystem()
