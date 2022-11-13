import { APP_INITIALIZER } from '@angular/core';
import { HomeFacade } from './home.facade';

export const HomeInitializer = (homeFacade: HomeFacade) => () => {
  homeFacade.fetchFlowGraph({
    successfulCallback: () => {},
  });
};

export const HomeInitializerProvider = {
  provide: APP_INITIALIZER,
  useFactory: HomeInitializer,
  multi: true,
  deps: [HomeFacade],
};
