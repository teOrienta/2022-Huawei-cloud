import Statistics from './statistics';

export interface UploadParams {
  analysisName: string;
  startTimestamp: string;
  timestamp: string;
  caseID: string;
  activity: string;
  orgResource: string;
}

interface fileSVG {
  path: string;
  status_code: number;
  filename: string;
  send_header_only: boolean;
  media_type: string;
  raw_headers: string[];
}

export interface uploadResponse {
  analysis_name: string;
  freq_svg: fileSVG;
  perf_svg: fileSVG;
  statistics: Statistics;
}
