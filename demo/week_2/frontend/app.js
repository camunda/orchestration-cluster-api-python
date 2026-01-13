// Configuration
const API_BASE_URL = 'http://localhost:8000';
// IMPORTANT: This must be the NUMERIC process_definition_key returned from deploying a BPMN process
// NOT the BPMN process ID. Example: "2251799813686749"
// You can get this by deploying a process via the /deploy/resource endpoint
const PROCESS_DEFINITION_KEY = '2251799813843646'; // Deployed loan application process

// Utility functions
function scrollToApplication() {
    document.getElementById('loans').scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    document.getElementById('loanApplicationForm').reset();
}

function resetStatus() {
    document.getElementById('statusPanel').style.display = 'none';
    document.getElementById('loanApplicationForm').style.display = 'flex';
    resetForm();
}

function showStatus(type, title, message, details = null) {
    const form = document.getElementById('loanApplicationForm');
    const statusPanel = document.getElementById('statusPanel');
    const statusIcon = document.getElementById('statusIcon');
    const statusTitle = document.getElementById('statusTitle');
    const statusMessage = document.getElementById('statusMessage');
    const processDetails = document.getElementById('processDetails');

    form.style.display = 'none';
    statusPanel.style.display = 'block';

    statusIcon.className = `status-icon ${type}`;
    statusTitle.textContent = title;
    statusMessage.textContent = message;

    if (details) {
        processDetails.innerHTML = `
            <h4>Process Details</h4>
            ${Object.entries(details).map(([key, value]) => `
                <div class="detail-row">
                    <span class="detail-label">${formatLabel(key)}:</span>
                    <span class="detail-value">${value}</span>
                </div>
            `).join('')}
        `;
    } else {
        processDetails.innerHTML = '';
    }
}

function formatLabel(key) {
    return key
        .replace(/_/g, ' ')
        .replace(/([A-Z])/g, ' $1')
        .replace(/^./, str => str.toUpperCase());
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(amount);
}

// API interaction
async function submitLoanApplication(formData) {
    try {
        // Prepare the variables for the Camunda process
        const processVariables = {
            applicantFirstName: formData.get('firstName'),
            applicantLastName: formData.get('lastName'),
            applicantEmail: formData.get('email'),
            applicantPhone: formData.get('phone'),
            loanAmount: parseFloat(formData.get('loanAmount')),
            loanPurpose: formData.get('loanPurpose'),
            annualIncome: parseFloat(formData.get('annualIncome')),
            employmentStatus: formData.get('employmentStatus'),
            creditScore: formData.get('creditScore') ? parseInt(formData.get('creditScore')) : null,
            applicationDate: new Date().toISOString(),
            applicationStatus: 'pending'
        };

        // Create the process instance
        const response = await fetch(`${API_BASE_URL}/loan-application`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                variables: processVariables
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create process instance');
        }

        const result = await response.json();

        // Debug logging
        console.log('API Response:', result);
        console.log('Response status field:', result.status);
        console.log('Response type:', typeof result.status);

        // Handle different response types based on status
        if (result.status === 'approved') {
            // Loan approved
            showStatus(
                'success',
                result.subject || 'Loan Application Approved!',
                result.message || 'Your loan application has been approved.',
                {
                    'Applicant': `${processVariables.applicantFirstName} ${processVariables.applicantLastName}`,
                    'Email': result.email || processVariables.applicantEmail,
                    'Loan Amount': formatCurrency(result.loanAmount || processVariables.loanAmount),
                    'Interest Rate': `${result.interestRate}%`,
                    'Risk Level': result.riskLevel,
                    'Status': 'Approved ✅'
                }
            );
        } else if (result.status === 'rejected') {
            // Loan rejected
            showStatus(
                'error',
                result.subject || 'Loan Application Status Update',
                result.message || 'Your loan application could not be approved at this time.',
                {
                    'Applicant': `${processVariables.applicantFirstName} ${processVariables.applicantLastName}`,
                    'Email': result.email || processVariables.applicantEmail,
                    'Loan Amount': formatCurrency(processVariables.loanAmount),
                    'Rejection Reason': result.rejectionReason || 'Not specified',
                    'Status': 'Rejected ❌'
                }
            );
        } else if (result.status === 'processing') {
            // Still processing after 10 seconds
            showStatus(
                'loading',
                result.subject || 'Application Received',
                result.message || 'Your application is being processed.',
                {
                    'Applicant': `${processVariables.applicantFirstName} ${processVariables.applicantLastName}`,
                    'Loan Amount': formatCurrency(processVariables.loanAmount),
                    'Purpose': processVariables.loanPurpose,
                    'Process Instance': result.process_instance_key,
                    'Status': 'Processing ⏳'
                }
            );
        } else {
            // Fallback for old format or unexpected response
            showStatus(
                'success',
                'Application Submitted Successfully!',
                `Your loan application for ${formatCurrency(processVariables.loanAmount)} has been received and is being processed.`,
                {
                    'Process Instance': result.process_instance_key || 'N/A',
                    'Applicant': `${processVariables.applicantFirstName} ${processVariables.applicantLastName}`,
                    'Loan Amount': formatCurrency(processVariables.loanAmount),
                    'Purpose': processVariables.loanPurpose,
                    'Status': 'Processing'
                }
            );
        }

        return result;
    } catch (error) {
        console.error('Error submitting application:', error);

        // Show error status
        showStatus(
            'error',
            'Application Submission Failed',
            error.message || 'An error occurred while processing your application. Please try again.',
            {
                'Error': error.message,
                'Timestamp': new Date().toLocaleString()
            }
        );

        throw error;
    }
}

// Form submission handler
document.getElementById('loanApplicationForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const submitButton = e.target.querySelector('.submit-button');
    submitButton.disabled = true;
    submitButton.textContent = 'Processing...';

    showStatus(
        'loading',
        'Processing Your Application',
        'Please wait while we submit your loan application...'
    );

    try {
        const formData = new FormData(e.target);
        await submitLoanApplication(formData);
    } catch (error) {
        // Error already handled in submitLoanApplication
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit Application';
    }
});

// Smooth scrolling for navigation links
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);

        if (targetSection) {
            targetSection.scrollIntoView({ behavior: 'smooth' });

            // Update active link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');
        }
    });
});

// Update active navigation link on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollPosition = window.scrollY + 100;

    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.offsetHeight;
        const sectionId = section.getAttribute('id');

        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Form validation feedback
document.querySelectorAll('input[required], select[required]').forEach(field => {
    field.addEventListener('invalid', (e) => {
        e.preventDefault();
        field.style.borderColor = 'var(--danger-color)';
    });

    field.addEventListener('input', () => {
        field.style.borderColor = 'var(--border-color)';
    });
});

// Log initialization
console.log('QuickLoan Bank Frontend initialized');
console.log('API Base URL:', API_BASE_URL);
console.log('Process Definition Key:', PROCESS_DEFINITION_KEY);
