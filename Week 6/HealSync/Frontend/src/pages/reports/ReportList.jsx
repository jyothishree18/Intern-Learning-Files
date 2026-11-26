
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  FileText,
  Search,
  Eye,
  Upload,
  RefreshCw,
} from "lucide-react";

import { getReports } from "../../services/reportService";

function ReportList() {
  const navigate = useNavigate();

  const [search, setSearch] = useState("");
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Fetch reports from FastAPI
  const fetchReports = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getReports();
      setReports(data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to load reports. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  // Search reports
  const filteredReports = reports.filter((report) =>
    `${report.report_code} ${report.patient_name || ""} ${report.patient_id} ${report.report_type}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="patients-page">

      {/* Page Header */}
      <div className="welcome-section">
        <h1>Medical Reports</h1>
        <p>View and manage hospital medical reports.</p>
      </div>

      {/* Toolbar */}
      <div className="patient-toolbar">

        <div className="patient-search">
          <Search size={18} />

          <input
            type="text"
            placeholder="Search reports or patients..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>

        <button
          className="add-patient-button"
          onClick={() => navigate("/reports/upload")}
        >
          <Upload size={17} />
          Upload Report
        </button>

        <button
          className="view-patient-button"
          onClick={fetchReports}
          disabled={loading}
        >
          <RefreshCw size={16} />
          Refresh
        </button>

      </div>

      {/* Report Table */}
      <div className="patient-table-card">

        <h2>
          <FileText size={21} />
          Report List ({filteredReports.length})
        </h2>

        {/* Loading */}
        {loading && (
          <p>Loading reports...</p>
        )}

        {/* Error */}
        {error && (
          <p role="alert" style={{ color: "red" }}>
            {error}
          </p>
        )}

        {/* Table */}
        {!loading && !error && (
          <div className="table-scroll">

            <table className="patient-table">

              <thead>
                <tr>
                  <th>Report ID</th>
                  <th>Patient Name</th>
                  <th>Report Type</th>
                  <th>Report Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>

                {filteredReports.length === 0 ? (

                  <tr>
                    <td colSpan="6">
                      No reports found.
                    </td>
                  </tr>

                ) : (

                  filteredReports.map((report) => (

                    <tr key={report.id}>

                      <td>
                        {report.report_code}
                      </td>

                      <td>
                        {report.patient_name ||
                          `Patient #${report.patient_id}`}
                      </td>

                      <td>
                        {report.report_type}
                      </td>

                      <td>
                        {report.report_date}
                      </td>

                      <td>
                        <span
                          className={`report-status ${report.status.toLowerCase()}`}
                        >
                          {report.status}
                        </span>
                      </td>

                      <td>
                        <button
                          className="view-patient-button"
                          onClick={() =>
                            navigate(`/reports/${report.id}`)
                          }
                        >
                          <Eye size={16} />
                          View
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

export default ReportList;
