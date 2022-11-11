import { APP_INITIALIZER } from '@angular/core';
import { FlowGraphParams } from '../shared/types/flow-graph-params';
import { HomeFacade } from './home.facade';

export const HomeInitializer = (homeFacade: HomeFacade) => () => {
  homeFacade.fetchFlowGraph({
    params: {} as FlowGraphParams,
    successfulCallback: () => {},
  });
};

export const HomeInitializerProvider = {
  provide: APP_INITIALIZER,
  useFactory: HomeInitializer,
  multi: true,
  deps: [HomeFacade],
};
