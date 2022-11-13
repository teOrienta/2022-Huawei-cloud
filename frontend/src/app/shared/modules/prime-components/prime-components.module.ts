import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CardModule } from 'primeng/card';
import { ButtonModule } from 'primeng/button';
import { CalendarModule } from 'primeng/calendar';
import { SliderModule } from 'primeng/slider';
import { SelectButtonModule } from 'primeng/selectbutton';
import { SkeletonModule } from 'primeng/skeleton';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SkeletonModule,
    SelectButtonModule,
  ],
  exports: [
    CalendarModule,
    CardModule,
    ButtonModule,
    SliderModule,
    SkeletonModule,
    SelectButtonModule,
  ],
})
export class PrimeComponentsModule {}
