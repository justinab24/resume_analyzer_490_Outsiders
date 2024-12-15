import React, { useState, useEffect } from 'react';
import { ProgressBar, ListGroup, Card, Button } from 'react-bootstrap';
import { PieChart, Pie, Cell, Tooltip } from 'recharts';
import jsPDF from 'jspdf';
import ResumeForm from './ResumeForm';
import Spinner from './Spinner';
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
  const [showDashboard, setShowDashboard] = useState(false);
  const [chartSize, setChartSize] = useState({
    width: Math.min(window.innerWidth * 0.8, 300),
    height: Math.min(window.innerHeight * 0.4, 200),
  });

  useEffect(() => {
    const handleResize = () => {
      setChartSize({
        width: Math.min(window.innerWidth * 0.8, 300),
        height: Math.min(window.innerHeight * 0.4, 200),
      });
    };
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const COLORS = ['#28a745', '#ffc107', '#dc3545'];
  const fitData = [
    { name: 'Matched Skills', value: fitScore.matched },
    { name: 'Partial Matches', value: fitScore.partial },
    { name: 'Missing Skills', value: fitScore.missing },
  ];

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
    <div id="dash" className="container my-5">
      {loading && <Spinner />}
      {!showDashboard && (
        <ResumeForm
          setFitScore={setFitScore}
          setMatchedSkills={setMatchedSkills}
          setImprovementSuggestions={setImprovementSuggestions}
          setLoading={setLoading}
          setShowDashboard={setShowDashboard}
        />
      )}
      {showDashboard && (
        <div className="dashboard-wrapper">
          <div className="dashboard-scrollable">
            <h2>Resume Analysis Dashboard</h2>
            <Card className="mt-4 mb-4">
              <Card.Body>
                <Card.Title>Resume Fit Score</Card.Title>
                <ProgressBar
                  now={fitScore.total}
                  label={`${fitScore.total}%`}
                  style={{
                    height: '20px',
                    backgroundColor: '#f4f4f4',
                    width: `${fitScore.total}%`,
                    background:
                      fitScore.total === 100 ? 'linear-gradient(135deg, #007bff, #0056b3)' :
                      fitScore.total <= 30 ? 'linear-gradient(135deg, #dc3545, #c82333)' :
                      fitScore.total <= 60 ? 'linear-gradient(135deg, #ffc107, #e0a800)' :
                      'linear-gradient(135deg, #28a745, #218838)',
                    transition: 'background 0.3s ease, width 0.3s ease',
                  }}
                  className="custom-progress-bar"
                />
                <div className="pie-chart-wrapper">
                  <PieChart width={chartSize.width} height={chartSize.height}>
                    <Pie
                      data={fitData}
                      cx="50%"
                      cy="50%"
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
            <div className="d-flex justify-content-between">
              <Button
                variant="success"
                onClick={generatePDF}
                disabled={loading || fitScore.total === 0}
              >
                Download PDF Report
              </Button>
              <Button variant="secondary" onClick={() => setShowDashboard(false)}>
                Go Back
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;