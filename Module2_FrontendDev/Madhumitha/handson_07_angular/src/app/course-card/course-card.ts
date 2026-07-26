import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-course-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <article class="course-card">
      <h3>{{ name }}</h3>
      <p>Code: <strong>{{ code }}</strong></p>
      <div class="card-footer">
        <span class="credits">Credits: {{ credits }}</span>
        <span class="grade">Grade: {{ grade }}</span>
      </div>
    </article>
  `,
  styles: [`
    .course-card { background:#fff; border:1px solid #d1dce8; border-radius:10px;
                   padding:20px; box-shadow:0 2px 8px rgba(0,0,0,.08); }
    .card-footer { display:flex; justify-content:space-between; margin-top:12px; }
    .credits { background:#e8f0fe; color:#0f3460; padding:3px 10px; border-radius:12px; font-size:0.8rem; }
    .grade { font-weight:700; color:#0f3460; }
  `]
})
export class CourseCardComponent {
  @Input() name!: string;
  @Input() code!: string;
  @Input() credits!: number;
  @Input() grade!: string;
}