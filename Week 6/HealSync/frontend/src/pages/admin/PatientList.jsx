
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Users,
  Search,
  RefreshCw,
  UserPlus,
  Eye,
} from "lucide-react";

import api from "../../services/api";

function PatientList() {
  const navigate = useNavigate();

  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const fetchPatients = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/patients");
      setPatients(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load patients."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPatients();
  }, []);

  const filteredPatients = patients.filter((patient) =>
    `${patient.patient_code} ${patient.full_name}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <h1>Patient Management</h1>
        <p>View and manage registered hospital patients.</p>
      </div>

      <div className="patient-toolbar">
        <div className="patient-search">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search by patient name or code..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <button onClick={fetchPatients} className="refresh-button">
          <RefreshCw size={17} />
          Refresh
        </button>

        <button
          onClick={() => navigate("/patients/add")}
          className="add-patient-button"
        >
          <UserPlus size={17} />
          Add New Patient
        </button>
      </div>

      <div className="patient-table-card">
        <h2>
          <Users size={20} />
          Patient List ({filteredPatients.length})
        </h2>

        {loading ? (
          <p>Loading patients...</p>
        ) : error ? (
          <p className="patient-error">{error}</p>
        ) : filteredPatients.length === 0 ? (
          <p>No patients found.</p>
        ) : (
          <div className="table-scroll">
            <table className="patient-table">
              <thead>
                <tr>
                  <th>Patient Code</th>
                  <th>Full Name</th>
                  <th>Age</th>
                  <th>Gender</th>
                  <th>Contact Number</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredPatients.map((patient) => (
                  <tr key={patient.id}>
                    <td>{patient.patient_code}</td>
                    <td>{patient.full_name}</td>
                    <td>{patient.age}</td>
                    <td>{patient.gender}</td>
                    <td>{patient.contact_number}</td>
                    <td>
                      <button
                        className="view-patient-button"
                        onClick={() =>
                          navigate(`/patients/${patient.id}`)
                        }
                      >
                        <Eye size={16} />
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientList;
