interface ErrorResult {
  error: string;
}

interface CheckResult {
  found: boolean;
  message: string;
  statusCode: number;
}

interface Metadata {
  titleValue: string | null;
  titleFound: boolean;
  descriptionValue: string | null;
  descriptionFound: boolean;
}

interface SeoResult {
  robots: CheckResult | ErrorResult;
  favicon: CheckResult | ErrorResult;
  sslCertificate: CheckResult | ErrorResult;
  metadata: Metadata | ErrorResult;
}

interface WordCloudResult {
  image: string;
}

interface Performance {
  performanceScore: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  cumulativeLayoutShift: number;
  totalBlockingTime: number;
}

export interface Analysis {
  seo: SeoResult;
  wordcloud: WordCloudResult | ErrorResult;
  performance: Performance | ErrorResult;
}
