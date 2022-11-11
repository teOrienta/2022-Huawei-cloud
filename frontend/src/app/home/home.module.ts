import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { HomeRoutingModule } from './home-routing.module';
import { HomeFacade } from './home.facade';
import { HomeInitializerProvider } from './home.initializer';
import { HomeComponent } from './pages/home/home.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { ForbiddenPageComponent } from './pages/forbidden-page/forbidden-page.component';

import { HomeState } from './state/home.state';
import { HomeApi } from './api/home.api';
import { HomeService } from './services/home.service';
import { FilterPageComponent } from './pages/filter-page/filter-page.component';
import { NavbarComponent } from './component/navbar/navbar.component';
import { FooterComponent } from './component/footer/footer.component';
import { FlowComponent } from './component/flow/flow.component';

@NgModule({
  declarations: [
    HomeComponent,
    NotFoundComponent,
    ForbiddenPageComponent,
    FilterPageComponent,
    NavbarComponent,
    FooterComponent,
    FlowComponent,
  ],
  imports: [HomeRoutingModule, SharedModule],
  providers: [
    HomeFacade,
    HomeState,
    HomeApi,
    HomeInitializerProvider,
    HomeService,
  ],
})
export class HomeModule {}
