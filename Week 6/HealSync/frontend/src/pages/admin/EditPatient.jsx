
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Save } from "lucide-react";

import api from "../../services/api";

function EditPatient() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    patient_code: "",
    full_name: "",
    age: "",
    gender: "",
    contact_number: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  // Load existing patient information
  useEffect(() => {
    const fetchPatient = async () => {
      try {
        const response = await api.get(`/patients/${id}`);

        setForm({
          patient_code: response.data.patient_code || "",
          full_name: response.data.full_name || "",
          age: response.data.age ?? "",
          gender: response.data.gender || "",
          contact_number: response.data.contact_number || "",
        });
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to load patient information."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchPatient();
  }, [id]);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  // Update patient information
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);

    try {
      await api.put(`/patients/${id}`, {
        ...form,
        age: Number(form.age),
      });

      alert("Patient details updated successfully!");
      navigate(`/patients/${id}`);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to update patient details."
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p>Loading patient information...</p>;
  }

  if (error && !form.patient_code) {
    return <p className="patient-error">{error}</p>;
  }

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <button
          className="back-button"
          onClick={() => navigate(`/patients/${id}`)}
        >
          <ArrowLeft size={17} />
          Back to Patient Details
        </button>

        <h1>Edit Patient</h1>
        <p>Update the registered patient's information.</p>
      </div>

      <form className="patient-form" onSubmit={handleSubmit}>
        <h2>Edit Patient Information</h2>

        <label>Patient Code</label>
        <input
          name="patient_code"
          value={form.patient_code}
          onChange={handleChange}
          required
        />

        <label>Full Name</label>
        <input
          name="full_name"
          value={form.full_name}
          onChange={handleChange}
          required
        />

        <label>Age</label>
        <input
          type="number"
          name="age"
          min="0"
          value={form.age}
          onChange={handleChange}
          required
        />

        <label>Gender</label>
        <select
          name="gender"
          value={form.gender}
          onChange={handleChange}
          required
        >
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>

        <label>Contact Number</label>
        <input
          type="tel"
          name="contact_number"
          value={form.contact_number}
          onChange={handleChange}
          required
        />

        {error && (
          <p className="patient-error">{error}</p>
        )}

        <button type="submit" disabled={saving}>
          <Save size={17} />
          {saving ? "Updating..." : "Save Changes"}
        </button>
      </form>
    </div>
  );
}

export default EditPatient;
