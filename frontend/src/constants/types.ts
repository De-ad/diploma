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

export interface Analysis {
  seo: SeoResult;
  keywordsDistribution: { [key: string]: any } | ErrorResult;
  wordcloud: WordCloudResult | ErrorResult;
  performance: Performance | ErrorResult;
  pageReport: PageReport[];
}

export interface KeywordsDistribution {
  title: any;
  description: any;
  headings: any;
  total: any;
}
