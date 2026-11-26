
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import {
  ArrowLeft,
  FileText,
  Download,
} from "lucide-react";

import {
  getReports,
  downloadReport,
} from "../../services/reportService";

function ReportDetails() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const reports = await getReports();

        const selectedReport = reports.find(
          (item) => String(item.id) === String(id)
        );

        if (!selectedReport) {
          setError("Report not found.");
          return;
        }

        setReport(selectedReport);
      } catch (err) {
        setError(
          err.response?.data?.detail ||
          "Unable to load report details."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchReport();
  }, [id]);

  const handleDownload = async () => {
    try {
      setDownloading(true);

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
      setDownloading(false);
    }
  };

  if (loading) {
    return <div className="patients-page">Loading report...</div>;
  }

  if (error || !report) {
    return (
      <div className="patients-page">
        <p>{error || "Report not found."}</p>
        <button
          className="back-button"
          onClick={() => navigate("/reports")}
        >
          <ArrowLeft size={17} />
          Back to Reports
        </button>
      </div>
    );
  }

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

        <h1>Report Details</h1>
        <p>View medical report information.</p>
      </div>

      <div className="patient-table-card">
        <h2>
          <FileText size={22} />
          {report.report_code}
        </h2>

        <div className="patient-details-grid">
          <div>
            <span>Report ID</span>
            <strong>{report.report_code}</strong>
          </div>

          <div>
            <span>Patient Name</span>
            <strong>
              {report.patient_name || "Name not available"}
            </strong>
          </div>

          <div>
            <span>Patient ID</span>
            <strong>{report.patient_id}</strong>
          </div>

          <div>
            <span>Report Type</span>
            <strong>{report.report_type}</strong>
          </div>

          <div>
            <span>Report Date</span>
            <strong>{report.report_date}</strong>
          </div>

          <div>
            <span>Status</span>
            <strong>{report.status}</strong>
          </div>

          <div>
            <span>Uploaded By</span>
            <strong>{report.uploaded_by}</strong>
          </div>

          <div>
            <span>File Name</span>
            <strong>{report.file_name}</strong>
          </div>

          <div>
            <span>File Size</span>
            <strong>
              {(report.file_size / 1024).toFixed(2)} KB
            </strong>
          </div>
        </div>

        <button
          className="add-patient-button"
          onClick={handleDownload}
          disabled={downloading}
        >
          <Download size={17} />
          {downloading ? "Downloading..." : "Download Report"}
        </button>
      </div>
    </div>
  );
}

export default ReportDetails;
