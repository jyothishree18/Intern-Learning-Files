
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Users,
  Search,
  RefreshCw,
  UserPlus,
  Trash2,
} from "lucide-react";

import api from "../../services/api";

function StaffList() {
  const navigate = useNavigate();

  const [staff, setStaff] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [search, setSearch] = useState("");

  const fetchStaff = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await api.get("/staff");
      setStaff(response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load staff."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStaff();
  }, []);

  const handleDelete = async (member) => {
    const confirmed = window.confirm(
      `Delete ${member.full_name}'s staff account?`
    );

    if (!confirmed) return;

    try {
      await api.delete(`/staff/${member.id}`);
      alert("Staff member deleted successfully!");
      fetchStaff();
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to delete staff member."
      );
    }
  };

  const filteredStaff = staff.filter((member) =>
    `${member.staff_code} ${member.full_name} ${member.role}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <h1>Staff Management</h1>
        <p>View and manage registered doctors and lab technicians.</p>
      </div>

      <div className="patient-toolbar">
        <div className="patient-search">
          <Search size={18} />
          <input
            type="text"
            placeholder="Search by name, code or role..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <button onClick={fetchStaff} className="refresh-button">
          <RefreshCw size={17} />
          Refresh
        </button>

        <button
          onClick={() => navigate("/staff/add")}
          className="add-patient-button"
        >
          <UserPlus size={17} />
          Add Staff
        </button>
      </div>

      <div className="patient-table-card">
        <h2>
          <Users size={20} />
          Staff List ({filteredStaff.length})
        </h2>

        {loading ? (
          <p>Loading staff...</p>
        ) : error ? (
          <p className="patient-error">{error}</p>
        ) : filteredStaff.length === 0 ? (
          <p>No staff members found.</p>
        ) : (
          <div className="table-scroll">
            <table className="patient-table">
              <thead>
                <tr>
                  <th>Staff Code</th>
                  <th>Full Name</th>
                  <th>Email</th>
                  <th>Contact Number</th>
                  <th>Role</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {filteredStaff.map((member) => (
                  <tr key={member.id}>
                    <td>{member.staff_code}</td>
                    <td>{member.full_name}</td>
                    <td>{member.email}</td>
                    <td>{member.contact_number}</td>
                    <td>
                      {member.role === "lab_tech"
                        ? "Lab Technician"
                        : "Doctor"}
                    </td>
                    <td>
                      <button
                        className="delete-patient-button"
                        onClick={() => handleDelete(member)}
                      >
                        <Trash2 size={16} />
                        Delete
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

export default StaffList;
