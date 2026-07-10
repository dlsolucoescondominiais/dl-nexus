// NO FIM do workflow (antes de responder)
const duration = Date.now() - $input.first().json._startTime;
const slaLimit = 3000; // 3s para chatbot
const slaBreached = duration > slaLimit;

// Registra métrica
await supabase.from('dl_nexus_metrics').insert({
  workflow_name: $workflow.name,
  execution_id: $execution.id,
  metric_type: 'duration',
  metric_value: duration,
  unit: 'ms',
  tags: { sla_limit: slaLimit, sla_breached: slaBreached }
});

// Se violou SLA -> alerta
if (slaBreached) {
  await $executeWorkflow({
    name: 'DL_MON_ALERTS',
    parameters: {
      alert_type: 'sla_breach',
      workflow: $workflow.name,
      execution_id: $execution.id,
      duration: duration,
      limit: slaLimit
    }
  });
}

return { json: { success: true, duration: duration, sla_breached: slaBreached } };
