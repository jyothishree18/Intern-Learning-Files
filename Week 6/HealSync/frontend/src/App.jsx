
import { useEffect, useState } from "react";
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate,
} from "react-router-dom";

import keycloak, { initKeycloak } from "./keycloak";

import DashboardLayout from "./layouts/DashboardLayout";

// Admin Pages
import AdminDashboard from "./pages/admin/AdminDashboard";
import PatientList from "./pages/admin/PatientList";
import AddPatient from "./pages/admin/AddPatient";
import PatientDetails from "./pages/admin/PatientDetails";
import EditPatient from "./pages/admin/EditPatient";
import StaffList from "./pages/admin/StaffList";
import AddStaff from "./pages/admin/AddStaff";

// Patient Dashboard
import PatientDashboard from "./pages/patient/PatientDashboard";

// Medical Reports
import ReportList from "./pages/reports/ReportList";
import UploadReport from "./pages/reports/UploadReport";
import ReportDetails from "./pages/reports/ReportDetails";

// Doctor and Lab Dashboards
function RoleDashboard({ role }) {
  const navigate = useNavigate();

  const isDoctor = role === "doctor";

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <h1>
          Welcome, {isDoctor ? "Doctor" : "Lab Technician"}!
        </h1>

        <p>
          {isDoctor
            ? "Manage patients and view their medical reports."
            : "Manage and upload hospital medical reports."}
        </p>
      </div>

      <div className="patient-table-card">
        <h2>
          {isDoctor ? "Doctor Dashboard" : "Lab Technician Dashboard"}
        </h2>

        <p>
          {isDoctor
            ? "Access patient information and medical reports."
            : "Upload and manage medical reports."}
        </p>

        <div
          style={{
            display: "flex",
            gap: "15px",
            flexWrap: "wrap",
            marginTop: "25px",
          }}
        >
          {isDoctor && (
            <button
              className="add-patient-button"
              onClick={() => navigate("/patients")}
            >
              View Patients
            </button>
          )}

          <button
            className="add-patient-button"
            onClick={() => navigate("/reports")}
          >
            View Medical Reports
          </button>

          <button
            className="view-patient-button"
            onClick={() => navigate("/reports/upload")}
          >
            Upload Report
          </button>
        </div>
      </div>
    </div>
  );
}

// Main App
function App() {
  const [ready, setReady] = useState(false);
  const [authenticated, setAuthenticated] = useState(false);

  useEffect(() => {
    initKeycloak()
      .then((isAuthenticated) => {
        setAuthenticated(isAuthenticated);
        setReady(true);
      })
      .catch((error) => {
        console.error("Keycloak initialization failed:", error);
        setReady(true);
      });
  }, []);

  if (!ready) {
    return <p>Loading HealSync...</p>;
  }

  if (!authenticated) {
    return (
      <div className="login-container">
        <h1>HealSync</h1>
        <p>Hospital Medical Report Management System</p>

        <button onClick={() => keycloak.login()}>
          Login to HealSync
        </button>
      </div>
    );
  }

  const roles =
    keycloak.tokenParsed?.realm_access?.roles || [];

  const appRole = [
    "admin",
    "doctor",
    "lab_tech",
    "patient",
  ].find((role) => roles.includes(role));

  const isAdmin = appRole === "admin";
  const isDoctor = appRole === "doctor";
  const isLabTech = appRole === "lab_tech";
  const isPatient = appRole === "patient";

  const canAccessReports = [
    "admin",
    "doctor",
    "lab_tech",
    "patient",
  ].includes(appRole);

  const canUploadReports = [
    "admin",
    "doctor",
    "lab_tech",
  ].includes(appRole);

  const canAccessPatients = [
    "admin",
    "doctor",
  ].includes(appRole);

  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DashboardLayout role={appRole} />}>

          {/* DASHBOARD */}
          <Route
            path="/dashboard"
            element={
              isAdmin ? (
                <AdminDashboard />
              ) : isPatient ? (
                <PatientDashboard />
              ) : isDoctor || isLabTech ? (
                <RoleDashboard role={appRole} />
              ) : (
                <h2>No role assigned to this account.</h2>
              )
            }
          />

          {/* PATIENT MANAGEMENT */}
          <Route
            path="/patients"
            element={
              canAccessPatients ? (
                <PatientList />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          <Route
            path="/patients/add"
            element={
              isAdmin ? (
                <AddPatient />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          <Route
            path="/patients/edit/:id"
            element={
              isAdmin ? (
                <EditPatient />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          <Route
            path="/patients/:id"
            element={
              canAccessPatients ? (
                <PatientDetails />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          {/* STAFF MANAGEMENT - ADMIN ONLY */}
          <Route
            path="/staff"
            element={
              isAdmin ? (
                <StaffList />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          <Route
            path="/staff/add"
            element={
              isAdmin ? (
                <AddStaff />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          {/* MEDICAL REPORTS */}
          <Route
            path="/reports"
            element={
              canAccessReports ? (
                isPatient ? (
                  <PatientDashboard />
                ) : (
                  <ReportList />
                )
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          {/* UPLOAD REPORT */}
          <Route
            path="/reports/upload"
            element={
              canUploadReports ? (
                <UploadReport />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          {/* REPORT DETAILS */}
          <Route
            path="/reports/:id"
            element={
              canUploadReports ? (
                <ReportDetails />
              ) : (
                <h2>Access restricted</h2>
              )
            }
          />

          {/* DEFAULT ROUTE */}
          <Route
            path="*"
            element={<Navigate to="/dashboard" replace />}
          />

        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
