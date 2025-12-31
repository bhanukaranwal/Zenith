import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  FolderKanban, 
  Database, 
  FlaskConical, 
  Package, 
  Rocket, 
  LineChart, 
  Bot,
  Menu,
  Moon,
  Sun,
  LogOut
} from 'lucide-react'
import { useAuthStore } from '../lib/stores/authStore'
import { useThemeStore } from '../lib/stores/themeStore'
import { cn } from '../lib/utils'

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Projects', href: '/projects', icon: FolderKanban },
  { name: 'Datasets', href: '/datasets', icon: Database },
  { name: 'Experiments', href: '/experiments', icon: FlaskConical },
  { name: 'Models', href: '/models', icon: Package },
  { name: 'Deployments', href: '/deployments', icon: Rocket },
  { name: 'Monitoring', href: '/monitoring', icon: LineChart },
  { name: 'Agents', href: '/agents', icon: Bot },
]

export default function Layout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const location = useLocation()
  const logout = useAuthStore((state) => state.logout)
  const user = useAuthStore((state) => state.user)
  const { theme, toggleTheme } = useThemeStore()

  return (
    <div className="min-h-screen bg-background">
      <div className={cn("fixed inset-y-0 left-0 z-50 w-64 bg-card border-r border-border transition-transform", !sidebarOpen && "-translate-x-full")}>
        <div className="flex h-16 items-center px-6 border-b border-border">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">
            Zenith
          </h1>
        </div>
        
        <nav className="flex-1 space-y-1 px-3 py-4">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={cn(
                  "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>
      </div>

      <div className={cn("transition-all", sidebarOpen ? "pl-64" : "pl-0")}>
        <header className="sticky top-0 z-40 flex h-16 items-center gap-4 border-b border-border bg-card px-6">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-muted-foreground hover:text-foreground"
          >
            <Menu className="h-6 w-6" />
          </button>

          <div className="flex-1" />

          <button
            onClick={toggleTheme}
            className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground"
          >
            {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
          </button>

          <div className="flex items-center gap-3">
            <span className="text-sm text-muted-foreground">{user?.username}</span>
            <button
              onClick={logout}
              className="rounded-md p-2 text-muted-foreground hover:bg-accent hover:text-accent-foreground"
            >
              <LogOut className="h-5 w-5" />
            </button>
          </div>
        </header>

        <main className="p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
