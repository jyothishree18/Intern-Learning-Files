
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  Download,
  RefreshCw,
  ShieldCheck,
} from "lucide-react";

import {
  getReports,
  downloadReport,
} from "../../services/reportService";

function PatientDashboard() {
  const navigate = useNavigate();

  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloadingId, setDownloadingId] = useState(null);

  const fetchReports = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getReports();
      setReports(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load your medical reports."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const patientName =
    reports.length > 0
      ? reports[0].patient_name || "Patient"
      : "Patient";

  const handleDownload = async (report) => {
    try {
      setDownloadingId(report.id);

      await downloadReport(
        report.id,
        report.file_name
      );
    } catch (err) {
      alert(
        err.response?.data?.detail ||
        "Unable to download report."
      );
    } finally {
      setDownloadingId(null);
    }
  };

  return (
    <div className="patients-page">
      <div className="welcome-section">
        <h1>Welcome, {patientName}!</h1>
        <p>
          View your personal medical reports and health records.
        </p>
      </div>

      <div className="patient-table-card">
        <h2>
          <ShieldCheck size={22} />
          Patient Dashboard
        </h2>

        <p>
          Your medical information is protected. You can access
          only reports linked to your patient account.
        </p>
      </div>

      <div className="patient-table-card">
        <div className="report-dashboard-heading">
          <h2>
            <FileText size={21} />
            My Medical Reports ({reports.length})
          </h2>

          <button
            className="view-patient-button"
            onClick={fetchReports}
            disabled={loading}
          >
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {loading && <p>Loading your reports...</p>}

        {error && (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        )}

        {!loading && !error && (
          <div className="table-scroll">
            <table className="patient-table">
              <thead>
                <tr>
                  <th>Report ID</th>
                  <th>Report Type</th>
                  <th>Report Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {reports.length === 0 ? (
                  <tr>
                    <td colSpan="5">
                      No medical reports available.
                    </td>
                  </tr>
                ) : (
                  reports.map((report) => (
                    <tr key={report.id}>
                      <td>{report.report_code}</td>
                      <td>{report.report_type}</td>
                      <td>{report.report_date}</td>
                      <td>{report.status}</td>
                      <td>
                        <button
                          className="view-patient-button"
                          onClick={() => handleDownload(report)}
                          disabled={downloadingId === report.id}
                        >
                          <Download size={16} />
                          {downloadingId === report.id
                            ? "Downloading..."
                            : "Download"}
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default PatientDashboard;
