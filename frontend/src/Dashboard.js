import React from 'react';
import { ProgressBar, ListGroup, Card } from 'react-bootstrap';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';

function Dashboard({ data }) {
  const { fitScore, matchedSkills, improvementSuggestions } = data;

  // Pie chart color scheme
  const COLORS = ['#28a745', '#ffc107', '#dc3545'];

  // Data for Pie Chart
  const fitData = [
    { name: 'Matched Skills', value: fitScore.matched },
    { name: 'Partial Matches', value: fitScore.partial },
    { name: 'Missing Skills', value: fitScore.missing },
  ];

  return (
    <div className="container my-4">
      <h2>Resume Analysis Dashboard</h2>

      {/* Resume Fit Score */}
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Resume Fit Score</Card.Title>
          <h4>{fitScore.total}% Match</h4>
          <ProgressBar now={fitScore.total} label={`${fitScore.total}%`} />
          <div className="mt-3">
            <h6>Skills Breakdown:</h6>
            <PieChart width={300} height={200}>
              <Pie
                data={fitData}
                cx={150}
                cy={100}
                innerRadius={40}
                outerRadius={80}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {fitData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </div>
        </Card.Body>
      </Card>

      {/* Skills and Keywords Matched */}
      <Card className="mb-4">
        <Card.Body>
          <Card.Title>Skills and Keywords Matched</Card.Title>
          <ListGroup>
            {matchedSkills.map((skill, index) => (
              <ListGroup.Item key={index}>
                <span className="text-success">✔</span> {skill}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>

      {/* Improvement Suggestions */}
      <Card>
        <Card.Body>
          <Card.Title>Improvement Suggestions</Card.Title>
          <ListGroup>
            {improvementSuggestions.map((suggestion, index) => (
              <ListGroup.Item key={index}>
                <span className="text-danger">⚠</span> {suggestion}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Dashboard;
