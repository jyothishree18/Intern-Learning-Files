
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  UserRound,
  Pencil,
  Trash2,
} from "lucide-react";

import api from "../../services/api";

function PatientDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [patient, setPatient] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const response = await api.get(`/patients/${id}`);
        setPatient(response.data);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to load patient details."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchPatient();
  }, [id]);

  const handleDelete = async () => {
    const confirmed = window.confirm(
      `Are you sure you want to delete ${patient.full_name}? This action cannot be undone.`
    );

    if (!confirmed) return;

    try {
      setDeleting(true);
      setError("");

      await api.delete(`/patients/${id}`);

      alert("Patient deleted successfully!");
      navigate("/patients");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to delete patient."
      );
      setDeleting(false);
    }
  };

  if (loading) return <p>Loading patient details...</p>;

  if (error && !patient) {
    return <p className="patient-error">{error}</p>;
  }

  if (!patient) return <p>Patient not found.</p>;

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <button
          className="back-button"
          onClick={() => navigate("/patients")}
        >
          <ArrowLeft size={17} />
          Back to Patients
        </button>

        <h1>Patient Details</h1>
        <p>View registered patient information.</p>
      </div>

      <div className="patient-table-card">
        <h2>
          <UserRound size={22} />
          {patient.full_name}
        </h2>

        <div className="patient-details-grid">
          <div>
            <span>Patient Code</span>
            <strong>{patient.patient_code}</strong>
          </div>

          <div>
            <span>Full Name</span>
            <strong>{patient.full_name}</strong>
          </div>

          <div>
            <span>Age</span>
            <strong>{patient.age}</strong>
          </div>

          <div>
            <span>Gender</span>
            <strong>{patient.gender}</strong>
          </div>

          <div>
            <span>Contact Number</span>
            <strong>{patient.contact_number}</strong>
          </div>
        </div>

        {error && (
          <p className="patient-error">{error}</p>
        )}

        <div className="patient-actions">
          <button
            className="add-patient-button"
            onClick={() => navigate(`/patients/edit/${id}`)}
          >
            <Pencil size={17} />
            Edit Patient
          </button>

          <button
            className="delete-patient-button"
            onClick={handleDelete}
            disabled={deleting}
          >
            <Trash2 size={17} />
            {deleting ? "Deleting..." : "Delete Patient"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default PatientDetails;
