import { NgModule } from '@angular/core';
import { SharedModule } from '../shared/shared.module';
import { HomeRoutingModule } from './home-routing.module';
import { HomeFacade } from './home.facade';
import { HomeInitializerProvider } from './home.initializer';
import { HomeComponent } from './pages/home/home.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';
import { ForbiddenPageComponent } from './pages/forbidden-page/forbidden-page.component';
import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { HomeState } from './state/home.state';
import { HomeApi } from './api/home.api';
import { HomeService } from './services/home.service';

@NgModule({
  declarations: [HomeComponent, NotFoundComponent, ForbiddenPageComponent],
  imports: [HomeRoutingModule, SharedModule, CardModule, ButtonModule],
  providers: [
    HomeFacade,
    HomeState,
    HomeApi,
    HomeInitializerProvider,
    HomeService,
  ],
})
export class HomeModule {}
