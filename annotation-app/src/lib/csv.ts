/**
 * CSV writing that matches Python's csv module defaults byte for byte:
 * minimal quoting (a field is quoted only if it contains a comma, a double
 * quote, CR or LF), doubled quotes inside quoted fields, CRLF after every
 * record, and no byte-order mark. scripts/calculate_agreement.py reads this.
 */

const NEEDS_QUOTING = /[",\r\n]/;

export function csvField(value: string): string {
  return NEEDS_QUOTING.test(value) ? `"${value.replace(/"/g, '""')}"` : value;
}

export function toCsv(columns: string[], rows: Record<string, string>[]): string {
  const records = [columns, ...rows.map((row) => columns.map((column) => row[column] ?? ''))];
  return records.map((record) => record.map(csvField).join(',') + '\r\n').join('');
}
