
import api from "./api";

// GET ALL REPORTS
export const getReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

// UPLOAD REPORT
export const uploadReport = async (formData) => {
  const response = await api.post(
    "/reports/upload",
    formData
  );
  return response.data;
};

// GET SINGLE REPORT
export const getReport = async (reportId) => {
  const response = await api.get(
    `/reports/${reportId}`
  );
  return response.data;
};

// DOWNLOAD ACTUAL REPORT FILE
export const downloadReport = async (reportId) => {
  const response = await api.get(
    `/reports/${reportId}/download`
  );

  const downloadUrl = response.data.download_url;

  if (!downloadUrl) {
    throw new Error("Download URL was not returned.");
  }

  // Open the actual file URL from storage
  const link = document.createElement("a");
  link.href = downloadUrl;
  link.target = "_blank";
  link.rel = "noopener noreferrer";

  document.body.appendChild(link);
  link.click();
  link.remove();
};
