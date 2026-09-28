export type Turn = {
  turn_id: number;
  speaker_id: string;
  speaker_role: string;
  text: string;
};

/** A pilot item as shipped to the app (see scripts/build_annotation_app_data.py). */
export type Item = {
  item_id: string;
  language: 'Hindi' | 'Hinglish';
  language_variety: string;
  source_type: string;
  context: Turn[];
  source_utterance: Turn;
  literal_gloss: string;
  listener_role: string;
  relationship: string;
  relative_status: string;
  familiarity: string;
  primary_phenomenon: string;
  secondary_phenomena: string[];
  speech_act: string;
  politeness_level: string;
  formality_level: string;
  stance: string;
  emotion: string;
  indirectness: string;
  code_switch_function: string | null;
  context_status: string;
  context_explanation: string;
  preservation_requirement: string;
  reference_translations: string[];
  acceptable_variants: string[];
  contrastive_translation: string;
  contrastive_error: string;
  contrastive_error_category: string;
  minimal_pair: boolean;
  hash: string;
};

/** One Stage 2 candidate: a translation of one item to be rated blind. */
export type Unit = {
  candidate_id: string;
  item_id: string;
  item_hash: string;
  /** Sheet context columns, precomputed in Python so the export matches exactly. */
  sheet: Record<string, string>;
};

export type DocEntry = { file: string; title: string; source_path: string };

export type Meta = {
  dataset_fingerprint: string;
  dataset_path: string;
  item_count: number;
  unit_count: number;
  stage2_enabled: boolean;
  calibration_items: string[];
  contact_instructions: string;
  review_columns: string[];
  stage2_columns: string[];
  stage2_context_columns: string[];
  stage2_evaluation_columns: string[];
  docs: DocEntry[];
};

export type Stage = 'stage1' | 'stage2';

/** Field name to answer. An empty string or a missing key means unanswered. */
export type Answers = Record<string, string>;

export type Response = {
  values: Answers;
  /** Hash of the item when this was answered; a mismatch means it was revised since. */
  itemHash: string;
  updatedAt: string;
  completedAt?: string;
};

export type LogEntry = { t: string; unit: string; field: string; from: string; to: string };

export type Session = {
  version: 1;
  stage: Stage;
  annotatorId: string;
  region: string;
  readinessConfirmed: boolean;
  datasetFingerprint: string;
  createdAt: string;
  updatedAt: string;
  /** Unit ids in presentation order, fixed when the session starts. */
  order: string[];
  position: number;
  /** Furthest position reached. Stage 2 never lets an annotator jump beyond it. */
  maxReached: number;
  responses: Record<string, Response>;
  checkpointPassed: boolean;
  calibrationLocked: boolean;
  breaksShown: number[];
  lastBackupAt?: string;
  lastBackupCompleted?: number;
  log: LogEntry[];
};
