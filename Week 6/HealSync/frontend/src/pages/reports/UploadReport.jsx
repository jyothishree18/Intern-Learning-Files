
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  ArrowLeft,
  Upload,
  FileText,
  X,
} from "lucide-react";

import { uploadReport } from "../../services/reportService";

function UploadReport() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    reportId: "",
    patientId: "",
    reportType: "",
    reportDate: "",
  });

  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!file) {
      setError("Please select a report file.");
      return;
    }

    const allowedTypes = [
      "application/pdf",
      "image/jpeg",
      "image/png",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError("Only PDF, JPEG and PNG files are allowed.");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError("File size must not exceed 10 MB.");
      return;
    }

    const formData = new FormData();

    formData.append("report_code", form.reportId);
    formData.append("patient_id", form.patientId);
    formData.append("report_type", form.reportType);
    formData.append("report_date", form.reportDate);
    formData.append("file", file);

    try {
      setLoading(true);

      await uploadReport(formData);

      alert("Medical report uploaded successfully!");
      navigate("/reports");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Report upload failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <button
          className="back-button"
          onClick={() => navigate("/reports")}
        >
          <ArrowLeft size={17} />
          Back to Reports
        </button>

        <h1>Upload Medical Report</h1>
        <p>Upload and associate a medical report with a patient.</p>
      </div>

      <form className="patient-form" onSubmit={handleSubmit}>
        <h2>
          <FileText size={21} />
          Report Information
        </h2>

        <label>Report ID</label>
        <input
          name="reportId"
          value={form.reportId}
          onChange={handleChange}
          placeholder="Example: RPT1003"
          required
        />

        <label>Patient ID</label>
        <input
          type="number"
          name="patientId"
          value={form.patientId}
          onChange={handleChange}
          placeholder="Enter existing patient database ID"
          min="1"
          required
        />

        <label>Report Type</label>
        <select
          name="reportType"
          value={form.reportType}
          onChange={handleChange}
          required
        >
          <option value="">Select Report Type</option>
          <option value="Blood Test">Blood Test</option>
          <option value="X-Ray">X-Ray</option>
          <option value="MRI Scan">MRI Scan</option>
          <option value="CT Scan">CT Scan</option>
          <option value="Urine Test">Urine Test</option>
          <option value="Other">Other</option>
        </select>

        <label>Report Date</label>
        <input
          type="date"
          name="reportDate"
          value={form.reportDate}
          onChange={handleChange}
          required
        />

        <label>Upload Report (PDF or Image)</label>

        <div className="report-upload-area">
          <Upload size={30} />

          <p>
            {file ? file.name : "Choose a PDF or PNG/JPEG file"}
          </p>

          <input
            type="file"
            accept=".pdf,.jpg,.jpeg,.png"
            onChange={(e) =>
              setFile(e.target.files[0] || null)
            }
            required
          />

          {file && (
            <button
              type="button"
              className="remove-file-button"
              onClick={() => setFile(null)}
            >
              <X size={15} />
              Remove file
            </button>
          )}
        </div>

        {error && (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        )}

        <button
          type="submit"
          className="add-patient-button"
          disabled={loading}
        >
          <Upload size={17} />
          {loading ? "Uploading..." : "Upload Report"}
        </button>
      </form>
    </div>
  );
}

export default UploadReport;
