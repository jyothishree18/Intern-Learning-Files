
import { NavLink, Outlet, useNavigate } from "react-router-dom";

import {
  LayoutDashboard,
  Users,
  FileText,
  Settings,
  LogOut,
  HeartPulse,
  Bell,
  UserCircle,
  Upload,
  UserCog,
} from "lucide-react";

import keycloak from "../keycloak";
import "../styles/dashboard.css";

function DashboardLayout({ role }) {
  const navigate = useNavigate();

  const navigation = [
    {
      name: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
    },

    // Patient Management - Admin and Doctor
    ...(role === "admin" || role === "doctor"
      ? [
          {
            name: "Patients",
            path: "/patients",
            icon: Users,
          },
        ]
      : []),

    // Staff Management - Admin Only
    ...(role === "admin"
      ? [
          {
            name: "Staff Management",
            path: "/staff",
            icon: UserCog,
          },
        ]
      : []),

    // Medical Reports - All Roles
    {
      name: "Medical Reports",
      path: "/reports",
      icon: FileText,
    },

    // Upload Reports - Admin, Doctor and Lab Technician
    ...(role === "admin" ||
    role === "doctor" ||
    role === "lab_tech"
      ? [
          {
            name: "Upload Report",
            path: "/reports/upload",
            icon: Upload,
          },
        ]
      : []),
  ];

  const username =
    keycloak.tokenParsed?.preferred_username || "User";

  const logout = () => {
    keycloak.logout({
      redirectUri: window.location.origin,
    });
  };

  return (
    <div className="dashboard-container">

      {/* SIDEBAR */}
      <aside className="sidebar">

        {/* BRAND */}
        <div className="brand">
          <HeartPulse size={30} />
          <span>HealSync</span>
        </div>

        {/* USER INFORMATION */}
        <div className="user-info">
          <UserCircle size={35} />

          <div>
            <strong>{username}</strong>
            <small>{role}</small>
          </div>
        </div>

        {/* NAVIGATION */}
        <nav className="sidebar-nav">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  isActive ? "nav-link active" : "nav-link"
                }
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* SIDEBAR BOTTOM */}
        <div className="sidebar-bottom">

          <button
            className="nav-link"
            onClick={() => navigate("/settings")}
          >
            <Settings size={19} />
            Settings
          </button>

          <button
            className="nav-link logout"
            onClick={logout}
          >
            <LogOut size={19} />
            Logout
          </button>

        </div>
      </aside>

      {/* MAIN CONTENT */}
      <main className="main-content">

        {/* TOPBAR */}
        <header className="topbar">
          <div>
            <h2>HealSync Portal</h2>
            <p>Hospital Medical Report Management System</p>
          </div>

          <div className="topbar-actions">
            <Bell size={21} />
            <UserCircle size={28} />
          </div>
        </header>

        {/* PAGE CONTENT */}
        <section className="page-content">
          <Outlet />
        </section>

      </main>
    </div>
  );
}

export default DashboardLayout;
