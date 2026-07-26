import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CourseCardComponent } from '../course-card/course-card';
import { CourseService, Course } from '../course';

@Component({
  selector: 'app-course-list',
  standalone: true,
  imports: [CommonModule, FormsModule, CourseCardComponent],
  template: `
    <div style="padding:40px 32px; max-width:1100px; margin:0 auto;">
      <h2>Enrolled Courses</h2>
      <input [(ngModel)]="searchTerm" placeholder="Search courses..."
             style="width:100%; max-width:400px; padding:10px; margin:16px 0;
                    border:1px solid #d1dce8; border-radius:6px; font-size:1rem;" />
      <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:20px;">
        <app-course-card
          *ngFor="let course of filteredCourses; trackBy: trackById"
          [name]="course.name"
          [code]="course.code"
          [credits]="course.credits"
          [grade]="course.grade">
        </app-course-card>
      </div>
      <p *ngIf="filteredCourses.length === 0">No courses found.</p>
    </div>
  `
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  searchTerm = '';

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.courseService.getCourses().subscribe(data => this.courses = data);
  }

  get filteredCourses(): Course[] {
    return this.courses.filter(c =>
      c.name.toLowerCase().includes(this.searchTerm.toLowerCase())
    );
  }

  trackById(_: number, course: Course): number { return course.id; }
}