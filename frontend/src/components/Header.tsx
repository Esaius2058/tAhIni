import { useNavigate, Link } from "react-router-dom";

export function Header() {
  const navigate = useNavigate();

  return (
    <header className="sticky top-0 z-50 w-full bg-[#f5f5f5] backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="w-full px-6 h-14 flex items-center justify-between">
        {/* Logo Container */}
        <div 
          className="cursor-pointer hover:opacity-80 transition-opacity" 
          onClick={() => navigate("/")}
        >
          <img
            src="/tAhIniLogoLight.svg"
            alt="logo"
            className="w-32 h-auto" 
          />
        </div>

        {/* Navigation Actions */}
        <nav className="flex items-center gap-4">
            <Link to="/login" className="hover:text-[#EC1C1B] font-medium">Login</Link>
            <Link to="/login" className="hover:text-[#EC1C1B] font-medium">Sign Up</Link>
        </nav>
      </div>
    </header>
  );
}