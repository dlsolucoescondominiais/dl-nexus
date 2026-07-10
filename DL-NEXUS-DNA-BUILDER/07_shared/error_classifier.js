function classifyError(errorMsg) {
  if (errorMsg.includes('credentials') || errorMsg.includes('expired')) return 'CREDENCIAL_EXPIRADA';
  if (errorMsg.includes('rate limit') || errorMsg.includes('429')) return 'API_RATE_LIMIT';
  if (errorMsg.includes('timeout')) return 'TIMEOUT';
  if (errorMsg.includes('permission') || errorMsg.includes('forbidden') || errorMsg.includes('403')) return 'PERMISSAO_NEGADA';
  return 'NODE_QUEBRADO';
}
module.exports = { classifyError };
