
import {
  Users,
  UserRound,
  FileText,
  Activity,
} from "lucide-react";

function AdminDashboard() {
  const stats = [
    {
      title: "Total Patients",
      value: "0",
      icon: Users,
    },
    {
      title: "Doctors",
      value: "0",
      icon: UserRound,
    },
    {
      title: "Medical Reports",
      value: "0",
      icon: FileText,
    },
    {
      title: "System Activity",
      value: "Active",
      icon: Activity,
    },
  ];

  return (
    <div>
      <div className="welcome-section">
        <h1>Admin Dashboard</h1>
        <p>Welcome to HealSync Hospital Management System.</p>
      </div>

      <div className="stats-grid">
        {stats.map((item) => {
          const Icon = item.icon;

          return (
            <div className="stat-card" key={item.title}>
              <div className="stat-icon">
                <Icon size={25} />
              </div>

              <div>
                <p>{item.title}</p>
                <h2>{item.value}</h2>
              </div>
            </div>
          );
        })}
      </div>

      <div className="dashboard-panel">
        <h2>Hospital Overview</h2>
        <p>
          Manage patients, doctors, medical reports,
          and hospital activities from one place.
        </p>
      </div>
    </div>
  );
}

export default AdminDashboard;
