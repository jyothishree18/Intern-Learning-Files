
import api from "./api";

export const getReports = async () => {
  const response = await api.get("/reports");
  return response.data;
};

export const uploadReport = async (formData) => {
  const response = await api.post("/reports/upload", formData);
  return response.data;
};

export const getReport = async (reportId) => {
  const response = await api.get(`/reports/${reportId}`);
  return response.data;
};

export const downloadReport = async (reportId, fileName) => {
  const response = await api.get(
    `/reports/${reportId}/download`,
    { responseType: "blob" }
  );

  const url = window.URL.createObjectURL(response.data);
  const link = document.createElement("a");

  link.href = url;
  link.download = fileName || `report-${reportId}`;
  document.body.appendChild(link);
  link.click();

  link.remove();
  window.URL.revokeObjectURL(url);
};
