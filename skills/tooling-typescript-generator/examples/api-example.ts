// TypeScript Express API Example: simple task API
// Demonstrates: typed routes, middleware, error handling, REST patterns

import express, { Request, Response, NextFunction } from 'express';

interface Task {
  id: number;
  title: string;
  completed: boolean;
}

const app = express();
app.use(express.json());

const tasks: Task[] = [];
let nextId = 1;

app.get('/tasks', (_req: Request, res: Response) => {
  res.json(tasks);
});

app.post('/tasks', (req: Request, res: Response) => {
  const task: Task = { id: nextId++, title: req.body.title, completed: false };
  tasks.push(task);
  res.status(201).json(task);
});

app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  res.status(500).json({ error: err.message });
});

app.listen(3000, () => console.log('API running on :3000'));
