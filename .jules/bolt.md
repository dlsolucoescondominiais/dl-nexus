## 2024-07-02 - Bolt Initialization
**Learning:** Initializing journal for Bolt.
**Action:** None.
## 2024-07-02 - Otimização de Renderização B2B no Supabase Realtime
**Learning:** Em componentes React que escutam canais em tempo real, computar KPIs da dashboard manualmente no método que busca os dados causa loops e manipulações de estado desnecessários a cada payload. Modificar kpis em useState junto de uma chamada de setLeads duplica renders no ciclo React.
**Action:** Usar useMemo na camada superior do componente atrelado ao array que compõe o estado principal do websocket, consolidando o single source of truth e impedindo recalculos desnecessários.
