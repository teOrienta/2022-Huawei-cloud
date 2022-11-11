import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { SelectButtonModule } from 'primeng/selectbutton';
import { AutoCompleteModule } from 'primeng/autocomplete';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
    AutoCompleteModule
  ],
  exports: [
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
    AutoCompleteModule
  ],
})
export class PrimeComponentsModule {}
