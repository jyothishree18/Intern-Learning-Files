
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft, UserPlus } from "lucide-react";
import api from "../../services/api";

function AddStaff() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    staff_code: "",
    full_name: "",
    email: "",
    contact_number: "",
    role: "",
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
      await api.post("/staff", form);

      alert("Staff account created successfully!");
      navigate("/staff");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to register staff member."
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
          onClick={() => navigate("/staff")}
        >
          <ArrowLeft size={17} />
          Back to Staff
        </button>

        <h1>Add New Staff</h1>
        <p>Register a doctor or lab technician and create their login account.</p>
      </div>

      <form className="patient-form" onSubmit={handleSubmit}>
        <h2>
          <UserPlus size={21} />
          Staff Information
        </h2>

        <label>Staff Code</label>
        <input
          name="staff_code"
          value={form.staff_code}
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

        <label>Email (Login Username)</label>
        <input
          type="email"
          name="email"
          value={form.email}
          onChange={handleChange}
          required
        />

        <label>Contact Number</label>
        <input
          type="tel"
          name="contact_number"
          value={form.contact_number}
          onChange={handleChange}
          required
        />

        <label>Staff Role</label>
        <select
          name="role"
          value={form.role}
          onChange={handleChange}
          required
        >
          <option value="">Select Role</option>
          <option value="doctor">Doctor</option>
          <option value="lab_tech">Lab Technician</option>
        </select>

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
          The staff member will be asked to change this password
          at their first login.
        </small>

        {error && (
          <p className="patient-error">{error}</p>
        )}

        <button type="submit" disabled={saving}>
          {saving ? "Creating Account..." : "Register Staff"}
        </button>
      </form>
    </div>
  );
}

export default AddStaff;
