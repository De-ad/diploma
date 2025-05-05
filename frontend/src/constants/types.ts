export interface ErrorResult {
  error: string;
}

export interface CheckResult {
  found: boolean;
  message: string;
  fileExtension?: string | null;
  statusCode: number;
}

export interface Metadata {
  titleValue: string | null;
  titleFound: boolean;
  descriptionValue: string | null;
  descriptionFound: boolean;
}

export interface Socials {
  titleValue?: string | null;
  titleFound?: boolean;
  typeValue?: string | null;
  typeFound?: boolean;
  descriptionValue?: string | null;
  descriptionFound?: boolean;
  imageValue?: string | null;
  imageFound?: boolean;
  urlValue?: string | null;
  urlFound?: boolean;
  twitterValue?: string | null;
  twitterFound?: boolean;
}

export interface SearchPreview {
  url: string;
  title?: string | null;
  description?: string | null;
  hasFavicon: boolean;
  date?: Date | null;
}

export interface SeoFiles {
  robots: CheckResult | ErrorResult;
  sitemap: CheckResult | ErrorResult;
  favicon: CheckResult | ErrorResult;
}

export interface SeoResult {
  seoFiles: SeoFiles;
  sslCertificate: CheckResult | ErrorResult;
  metadata: Metadata | ErrorResult;
  socials: Socials | ErrorResult;
  searchPreview: SearchPreview | ErrorResult;
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

export interface Performance {
  mobile: PerformanceMetrics;
  desktop: PerformanceMetrics;
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
}

export interface PageReport {
  url: string;
  issues: PageIssues;
}

export interface Analysis {
  seo: SeoResult;
  keywordsDestribution: { [key: string]: any } | ErrorResult;
  wordcloud: WordCloudResult | ErrorResult;
  performance: Performance | ErrorResult;
  pageReport: PageReport[];
}

export interface KeywordsDestribution {
  title: any;
  description: any;
  headings: any;
  total: any;
}
