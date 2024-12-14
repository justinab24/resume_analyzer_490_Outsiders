import React, { useState } from 'react';
import { ProgressBar, ListGroup, Card, Button, } from 'react-bootstrap';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';
import jsPDF from 'jspdf';
import ResumeForm from './ResumeForm';
import '../stylesheet/dashboard.css';



function Dashboard() {
  const [loading, setLoading] = useState(false);
  const [fitScore, setFitScore] = useState({
    total: 0,
    matched: 0,
    partial: 0,
    missing: 0,
  });
  const [matchedSkills, setMatchedSkills] = useState([]);
  const [improvementSuggestions, setImprovementSuggestions] = useState([]);
  const [showDashboard, setShowDashboard] = useState(false);  // Track whether the dashboard should be shown
  // Pie chart color scheme
  const COLORS = ['#28a745', '#ffc107', '#dc3545'];

  // Data for Pie Chart
  const fitData = [
    { name: 'Matched Skills', value: fitScore.matched },
    { name: 'Partial Matches', value: fitScore.partial },
    { name: 'Missing Skills', value: fitScore.missing },
  ];

  // Generate PDF
  const generatePDF = () => {
    const doc = new jsPDF();
    doc.text('Resume Analysis Report', 10, 10);
    doc.text(`Fit Score: ${fitScore.total}%`, 10, 20);
    doc.text('Matched Keywords:', 10, 30);
    matchedSkills.forEach((keyword, index) => {
      doc.text(`- ${keyword}`, 10, 40 + index * 10);
    });
    doc.text('Improvement Suggestions:', 10, 60 + matchedSkills.length * 10);
    improvementSuggestions.forEach((suggestion, index) => {
      doc.text(`- ${suggestion}`, 10, 70 + matchedSkills.length * 10 + index * 10);
    });
    doc.save('Resume_Analysis_Report.pdf');
  };

  return (
    <div className="container my-4">
      <ResumeForm
        setFitScore={setFitScore}
        setMatchedSkills={setMatchedSkills}
        setImprovementSuggestions={setImprovementSuggestions}
        setLoading={setLoading}
        setShowDashboard={setShowDashboard}
      />

      {/* Conditionally Render Dashboard */}
      {showDashboard && (
        <>
          <h2>Resume Analysis Dashboard</h2>

          <Card className="mt-4 mb-4">
            <Card.Body>
              <Card.Title>Resume Fit Score</Card.Title>
              <ProgressBar
                  now={fitScore.total}  // Percentage of progress
                  label={`${fitScore.total}%`}  // Percentage inside the bar
                  style={{
                    height: '20px',
                    backgroundColor: '#f4f4f4',  // Empty portion
                    width: `${fitScore.total}%`,  // Dynamic width based on fitScore.total
                    background: 
                      fitScore.total === 100 ? 'linear-gradient(135deg, #007bff, #0056b3)' : // Blue for 100%
                      fitScore.total <= 30 ? 'linear-gradient(135deg, #dc3545, #c82333)' :     // Red for <= 30%
                      fitScore.total <= 60 ? 'linear-gradient(135deg, #ffc107, #e0a800)' :    // Yellow for 31-60%
                      'linear-gradient(135deg, #28a745, #218838)',  // Green for > 60%
                    transition: 'background 0.3s ease, width 0.3s ease',
                  }}
                  className="custom-progress-bar"
                />


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
          <Card className="mb-4">
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

          {/* Download PDF Report */}
          <Button variant="success" onClick={generatePDF} disabled={loading || fitScore.total === 0}>
            Download PDF Report
          </Button>
        </>
      )}
    </div>
  );
}

export default Dashboard;