import React from 'react'
import { useAuth } from '../../lib/auth'
import { Menu, User, LogOut, Sun, Moon } from 'lucide-react'
import { cn } from '../../lib/utils'

interface HeaderProps {
  onMenuToggle: () => void
  isDarkMode: boolean
  onThemeToggle: () => void
}

export const Header: React.FC<HeaderProps> = ({ 
  onMenuToggle, 
  isDarkMode, 
  onThemeToggle 
}) => {
  const { user, signOut } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200 px-4 py-3">
      <div className="flex items-center justify-between">
        {/* Left side - Menu toggle */}
        <button
          onClick={onMenuToggle}
          className="p-2 rounded-lg hover:bg-gray-100 lg:hidden"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Right side - User actions */}
        <div className="flex items-center gap-4">
          {/* Theme toggle */}
          <button
            onClick={onThemeToggle}
            className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            title={isDarkMode ? "Modo claro" : "Modo escuro"}
          >
            {isDarkMode ? (
              <Sun className="w-5 h-5" />
            ) : (
              <Moon className="w-5 h-5" />
            )}
          </button>

          {/* User menu */}
          <div className="flex items-center gap-3">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">
                {user?.user_metadata?.name || user?.email || 'Usuário'}
              </p>
              <p className="text-xs text-gray-500">
                {user?.email || 'guest@vcm.com'}
              </p>
            </div>
            
            <div className="relative group">
              <button className="p-2 rounded-lg hover:bg-gray-100 transition-colors">
                <User className="w-5 h-5" />
              </button>
              
              {/* Dropdown menu */}
              <div className={cn(
                "absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1",
                "opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200"
              )}>
                <button
                  onClick={signOut}
                  className="flex items-center gap-2 w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                >
                  <LogOut className="w-4 h-4" />
                  Sair
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}