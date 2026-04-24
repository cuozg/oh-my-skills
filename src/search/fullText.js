const TOKEN_PATTERN = /[a-z0-9]+/g;

export function normalizeText(value) {
  return String(value ?? "")
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

export function tokenize(value) {
  return normalizeText(value).match(TOKEN_PATTERN) ?? [];
}

export function stemToken(token) {
  if (token.length > 5 && token.endsWith("ing")) {
    return token.slice(0, -3);
  }

  if (token.length > 4 && token.endsWith("es")) {
    return token.slice(0, -2);
  }

  if (token.length > 3 && token.endsWith("s")) {
    return token.slice(0, -1);
  }

  return token;
}

export function scoreFullTextRecord({ record, fields, terms, query }) {
  const normalizedQuery = normalizeText(query);

  return fields.reduce(
    (scoreState, field) => {
      const fieldValue = record[field.name];
      const normalizedField = normalizeText(fieldValue);
      const tokens = tokenize(fieldValue);
      const fieldScore = scoreField({ tokens, terms, weight: field.weight });
      const phraseScore =
        normalizedQuery.length > 0 && normalizedField.includes(normalizedQuery)
          ? field.weight * terms.length
          : 0;
      const totalFieldScore = fieldScore + phraseScore;

      if (totalFieldScore <= 0) {
        return scoreState;
      }

      return {
        score: scoreState.score + totalFieldScore,
        matchedFields: [...scoreState.matchedFields, field.name]
      };
    },
    { score: 0, matchedFields: [] }
  );
}

function scoreField({ tokens, terms, weight }) {
  return terms.reduce((termScore, term) => {
    const tokenScore = tokens.reduce((currentTokenScore, token) => {
      const comparableToken = stemToken(token);
      const comparableTerm = stemToken(term);

      if (comparableToken === comparableTerm) {
        return currentTokenScore + weight * 3;
      }

      if (comparableToken.startsWith(comparableTerm)) {
        return currentTokenScore + weight * 2;
      }

      if (comparableToken.includes(comparableTerm)) {
        return currentTokenScore + weight;
      }

      return currentTokenScore;
    }, 0);

    return termScore + tokenScore;
  }, 0);
}

export function sortByRelevanceThenId(left, right) {
  if (right.score !== left.score) {
    return right.score - left.score;
  }

  return String(left.id).localeCompare(String(right.id));
}
