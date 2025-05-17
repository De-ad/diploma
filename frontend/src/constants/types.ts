export interface ErrorResult {
  error: string;
}

export interface CheckResult {
  found: boolean;
  message?: string | null;
  fileExtension?: string | null;
  statusCode?: number | null;
  error?: string | null;
}

export interface Metadata {
  title: string | null;
  description: string | null;
}

export interface Socials {
  titleValue?: string | null;
  typeValue?: string | null;
  descriptionValue?: string | null;
  imageValue?: string | null;
  urlValue?: string | null;
  twitterValue?: string | null;
}

export interface SearchPreview {
  url: string;
  title?: string | null;
  description?: string | null;
  hasFavicon: boolean;
  date?: Date | null;
}

export interface SeoFiles {
  robots: CheckResult;
  sitemap: CheckResult;
  favicon: CheckResult;
}

export interface SeoResult {
  seoFiles: SeoFiles;
  sslCertificate: CheckResult;
  metadata: Metadata | ErrorResult;
  socials: Socials | ErrorResult;
  searchPreview: SearchPreview | ErrorResult;
  spfRecord: CheckResult;
  canonicalUrl?: string | null;
  structuredData?: Array<Record<string, any>>;
  charset?: string | null;
  doctype?: string | null;
}

export interface WordCloudResult {
  data: Array<{ [key: string]: string | number }>;
}

export interface PerformanceMetrics {
  performanceScore: number;
  firstContentfulPaint: string;
  largestContentfulPaint: string;
  cumulativeLayoutShift: string;
  totalBlockingTime: string;
  speedIndex: string;
}

export interface ImageInfo {
  src: string;
  sizeKb: number;
}

export interface AssetIssues {
  uncachedJs: string[];
  unminifiedJs: string[];
  uncachedCss: string[];
  unminifiedCss: string[];
}

export interface HtmlCompression {
  uncompressedSizeKb: number;
  compressedSizeKb: number;
  compressionType: string;
  compressionRatePercent: number;
}

export interface DataMetrics {
  domSize: number;
  htmlCompression: HtmlCompression;
  totalImages: number;
  oversizedImages: ImageInfo[];
  uncachedImages: string[];
  assetIssues: AssetIssues;
}

export interface Performance {
  mobile: PerformanceMetrics;
  desktop: PerformanceMetrics;
  dataMetrics: DataMetrics;
}

export interface BrokenLink {
  link: string;
  error: string;
}

export interface PageIssues {
  h1Missing?: boolean | null;
  inlineCode?: boolean | null;
  imageSeo?: string[] | null;
  brokenLinks?: BrokenLink[] | null;
  noindex?: boolean | null;
  flashContent?: boolean | null;
  framesetUsed?: boolean | null;
  unsafeLinks?: string[] | null;
}

export interface PageReport {
  url: string;
  issues: PageIssues;
}

export interface SslCertificate {
  subject: string;
  issuer: string;
  notValidBefore: string;
  notValidAfter: string;
  signatureAlgorithm: string;
  version: string;
}

interface SslChecks {
  notUsedBeforeActivationDate: boolean;
  notExpired: boolean;
  hostnameMatches: boolean;
  trustedByMajorBrowsers: boolean;
  usesSecureHash: boolean;
}

interface SslCertificatesAndChecks {
  serverCertificate: SslCertificate;
  intermediateCertificates: SslCertificate[];
  rootCertificate: SslCertificate;
  checks: SslChecks;
}
export interface Security {
  sslCertificates: SslCertificatesAndChecks;
  spfRecord: CheckResult;
  allUnsafeLinks: string[];
  http2Support: boolean;
}

export interface Score {
  seo: number;
  performance: number;
  security: number;
}

export interface Analysis {
  seo: SeoResult;
  keywordsDistribution: { [key: string]: any } | ErrorResult;
  wordcloud: WordCloudResult | ErrorResult;
  performance: Performance | ErrorResult;
  pageReport: PageReport[];
  security: Security;
  score: Score;
}

export interface KeywordsDistribution {
  title: any;
  description: any;
  headings: any;
  total: any;
}

export interface DesignAnalysis {
  message: {
    criteria: {
      attribute: string;
      grade: string;
      output: string;
    }[];
    finalGrade: string;
  };
}

export interface ImageData {
  dataURL: string;
  fileName: string;
}
