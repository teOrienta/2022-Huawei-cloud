import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { CsvImportationComponent } from './pages/csv-importation/csv-importation.component';
import { FilterPageComponent } from './pages/filter-page/filter-page.component';
import { ForbiddenPageComponent } from './pages/forbidden-page/forbidden-page.component';
import { HomeComponent } from './pages/home/home.component';
import { NotFoundComponent } from './pages/not-found/not-found.component';

const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
  },
  {
    path: 'filter',
    component: FilterPageComponent,
  },
  {
    path: 'importation',
    component: CsvImportationComponent
  },
  {
    path: 'forbidden',
    component: ForbiddenPageComponent,
  },
  {
    path: '**',
    component: NotFoundComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class HomeRoutingModule {}
