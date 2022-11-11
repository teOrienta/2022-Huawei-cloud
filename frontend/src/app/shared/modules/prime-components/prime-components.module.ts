import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { SelectButtonModule } from 'primeng/selectbutton';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
  ],
  exports: [
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SelectButtonModule,
  ],
})
export class PrimeComponentsModule {}
