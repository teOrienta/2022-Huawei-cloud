interface FlowGraphParams {
  start_date: string | null | undefined;
  end_date: string | null | undefined;
}

interface FetchFlowGraph {
  params: FlowGraphParams;
  successfulCallback: () => void;
}

export { FetchFlowGraph, FlowGraphParams };
