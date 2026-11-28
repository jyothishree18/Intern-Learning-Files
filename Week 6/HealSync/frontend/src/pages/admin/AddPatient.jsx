
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, UserPlus } from "lucide-react";
import api from "../../services/api";

function AddPatient() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    patient_code: "",
    full_name: "",
    age: "",
    gender: "",
    contact_number: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSaving(true);

    try {
      await api.post("/patients", {
        ...form,
        age: Number(form.age),
      });

      alert(
        "Patient registered successfully! Login account created."
      );

      navigate("/patients");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to register patient."
      );
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <button
          className="back-button"
          onClick={() => navigate("/patients")}
        >
          <ArrowLeft size={17} /> Back to Patients
        </button>

        <h1>Add New Patient</h1>
        <p>
          Register patient information and create their login account.
        </p>
      </div>

      <form className="patient-form" onSubmit={handleSubmit}>
        <h2>
          <UserPlus size={21} /> Patient Information
        </h2>

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
          max="130"
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

        <label>Email (Login Username)</label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label>Initial Password</label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          minLength={8}
          required
        />

        <small>
          The patient will be asked to change this password
          at their first login.
        </small>

        {error && (
          <p className="patient-error">{error}</p>
        )}

        <button type="submit" disabled={saving}>
          {saving ? "Creating Account..." : "Register Patient"}
        </button>
      </form>
    </div>
  );
}

export default AddPatient;
