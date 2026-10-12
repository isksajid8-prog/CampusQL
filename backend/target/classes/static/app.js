const app = document.getElementById('app');
const state = { user: null, dashboard: null };

async function request(path, options = {}) {
    const defaultOptions = {
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
    };

    const merged = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...(options.headers || {})
        }
    };

    const csrfCookie = document.cookie.split('; ').find(row => row.startsWith('XSRF-TOKEN='));
    if (csrfCookie && !merged.headers['X-XSRF-TOKEN']) {
        merged.headers['X-XSRF-TOKEN'] = decodeURIComponent(csrfCookie.split('=')[1]);
    }

    if (['POST', 'PUT', 'PATCH', 'DELETE'].includes((options.method || 'GET').toUpperCase()) && !merged.headers['X-XSRF-TOKEN']) {
        try {
            const csrfResponse = await fetch('/api/auth/csrf', { method: 'GET', credentials: 'same-origin' });
            const csrfCookie2 = document.cookie.split('; ').find(row => row.startsWith('XSRF-TOKEN='));
            if (csrfCookie2) {
                merged.headers['X-XSRF-TOKEN'] = decodeURIComponent(csrfCookie2.split('=')[1]);
            }
        } catch (error) {
            console.warn('CSRF lookup failed', error);
        }
    }

    const response = await fetch(path, merged);
    const contentType = response.headers.get('content-type') || '';
    const payload = contentType.includes('application/json') ? await response.json() : await response.text();

    if (!response.ok) {
        throw new Error(payload.message || 'Request failed');
    }

    return payload;
}

function setAlert(message, kind = 'info') {
    const alertBox = document.getElementById('alertBox');
    alertBox.className = `alert ${kind}`;
    alertBox.textContent = message;
}

function renderAuth() {
    app.innerHTML = `
      <div class="topbar">
        <div><strong>CampusIQ</strong> Secure Student Portal</div>
        <span class="badge">Synthetic roster enabled</span>
      </div>
      <div class="container">
        <div class="hero">
          <div class="card">
            <h1>Smart campus analytics for secure academic visibility</h1>
            <p class="muted">Students, faculty, and administrators work from a verified identity model that protects private academic records.</p>
            <div class="metric-grid">
              <div class="metric"><strong>92.5%</strong><div>Average attendance</div></div>
              <div class="metric"><strong>8.7</strong><div>CGPA trend</div></div>
              <div class="metric"><strong>3</strong><div>Verified students</div></div>
            </div>
          </div>
          <div class="card">
            <div class="inline" style="margin-bottom:18px;">
              <button class="secondary" data-auth-tab="login">Login</button>
              <button class="secondary" data-auth-tab="register">Register</button>
            </div>
            <div id="alertBox" class="alert info">Use the demo accounts below to explore the system.</div>
            <div id="loginPanel">
              <h3>Login</h3>
              <div class="form-grid">
                <div class="form-field">
                  <label>Email</label>
                  <input id="loginEmail" type="email" placeholder="college email">
                </div>
                <div class="form-field">
                  <label>Password</label>
                  <input id="loginPassword" type="password" placeholder="password">
                </div>
              </div>
              <div style="margin-top:16px;">
                <button id="loginButton">Login</button>
              </div>
              <p class="muted">Demo accounts: admin@campus.edu / Campus@123, faculty@campus.edu / Campus@123</p>
            </div>
            <div id="registerPanel" class="hidden">
              <h3>Student Registration</h3>
              <div class="form-grid">
                <div class="form-field"><label>Student ID</label><input id="studentId" value="2024001"></div>
                <div class="form-field"><label>Full name</label><input id="fullName" value="Aisha Khan"></div>
                <div class="form-field"><label>College email</label><input id="email" type="email" value="aisha.khan@campus.edu"></div>
                <div class="form-field"><label>Department</label><input id="department" value="Computer Science"></div>
                <div class="form-field"><label>Academic year</label><input id="academicYear" value="2024"></div>
                <div class="form-field"><label>Current semester</label><input id="semester" value="6"></div>
                <div class="form-field"><label>Password</label><input id="password" type="password" value="Campus@123"></div>
                <div class="form-field"><label>Confirm password</label><input id="confirmPassword" type="password" value="Campus@123"></div>
                <div class="form-field"><label>Phone</label><input id="phone" value="+91-90000-1001"></div>
                <div class="form-field"><label>Profile image</label><input id="profileImage" value=""></div>
              </div>
              <label style="display:block; margin-top:12px;">
                <input id="termsAccepted" type="checkbox" checked> I accept the terms and conditions.
              </label>
              <div style="margin-top:16px;">
                <button id="registerButton">Submit Registration</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    `;

    document.querySelectorAll('[data-auth-tab]').forEach(btn => {
        btn.onclick = () => {
            const tab = btn.dataset.authTab;
            document.getElementById('loginPanel').classList.toggle('hidden', tab !== 'login');
            document.getElementById('registerPanel').classList.toggle('hidden', tab !== 'register');
        };
    });

    document.getElementById('loginButton').onclick = async () => {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;
        try {
            const result = await request('/api/auth/login', {
                method: 'POST',
                body: JSON.stringify({ email, password })
            });
            loadUser();
            setAlert(result.message, 'success');
        } catch (err) {
            setAlert(err.message, 'error');
        }
    };

    document.getElementById('registerButton').onclick = async () => {
        const payload = {
            studentId: document.getElementById('studentId').value,
            fullName: document.getElementById('fullName').value,
            email: document.getElementById('email').value,
            department: document.getElementById('department').value,
            academicYear: document.getElementById('academicYear').value,
            semester: document.getElementById('semester').value,
            password: document.getElementById('password').value,
            confirmPassword: document.getElementById('confirmPassword').value,
            phone: document.getElementById('phone').value,
            profileImage: document.getElementById('profileImage').value,
            termsAccepted: document.getElementById('termsAccepted').checked ? 'true' : 'false'
        };

        try {
            const result = await request('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            setAlert(result.message, 'success');
        } catch (err) {
            setAlert(err.message, 'error');
        }
    };
}

async function loadUser() {
    try {
        const profile = await request('/api/auth/me');
        state.user = profile;
        renderDashboard();
    } catch (error) {
        state.user = null;
        renderAuth();
    }
}

function renderDashboard() {
    const role = state.user.role;
    const userName = state.user.name;
    app.innerHTML = `
      <div class="topbar">
        <div><strong>CampusIQ</strong> ${userName}</div>
        <div class="inline">
          <span class="badge">${role}</span>
          <button class="danger" id="logoutButton">Logout</button>
        </div>
      </div>
      <div class="container">
        <div class="card" style="margin-top:24px;">
          <h2>Welcome, ${userName}</h2>
          <p class="muted">${role} access • ${state.user.department || 'Institutional'} • ${state.user.studentId || ''}</p>
          <div id="dashboardContent"></div>
        </div>
      </div>
    `;

    document.getElementById('logoutButton').onclick = async () => {
        await request('/api/auth/logout', { method: 'POST' });
        state.user = null;
        renderAuth();
    };

    if (role === 'STUDENT') {
        fetchStudentDashboard();
    } else if (role === 'FACULTY') {
        fetchFacultyDashboard();
    } else {
        fetchAdminDashboard();
    }
}

async function fetchStudentDashboard() {
    try {
        const data = await request('/api/student/dashboard');
        state.dashboard = data;
        const subjectRows = Object.entries(data.subjectMarks || {}).map(([subject, score]) => `
          <tr><td>${subject}</td><td>${score}</td><td>${data.subjectAttendance?.[subject] ?? 0}%</td></tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <div class="metric-grid">
            <div class="metric"><strong>${data.attendancePercentage}%</strong><div>Attendance</div></div>
            <div class="metric"><strong>${data.cgpa}</strong><div>CGPA</div></div>
            <div class="metric"><strong>${data.studentSuccessScore}</strong><div>Success score</div></div>
            <div class="metric"><strong>${data.placementReadiness}</strong><div>Placement readiness</div></div>
          </div>
          <h3 style="margin-top:24px;">Academic performance</h3>
          <table class="table">
            <thead><tr><th>Subject</th><th>Marks</th><th>Attendance</th></tr></thead>
            <tbody>${subjectRows}</tbody>
          </table>
          <h3 style="margin-top:24px;">Risk indicators & suggestions</h3>
          <ul>${(data.riskIndicators || []).map(item => `<li>${item}</li>`).join('')}</ul>
          <ul>${(data.improvementSuggestions || []).map(item => `<li>${item}</li>`).join('')}</ul>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

async function fetchFacultyDashboard() {
    try {
        const data = await request('/api/faculty/overview');
        const rows = (data.assignedStudents || []).map(student => `
            <tr>
              <td>${student.fullName}</td>
              <td>${student.studentId}</td>
              <td>${student.studentSuccessScore}</td>
              <td>${student.riskIndicators[0] || 'No major risk'}</td>
            </tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <h3>Assigned student cohort</h3>
          <table class="table"><thead><tr><th>Student</th><th>ID</th><th>Success Score</th><th>Risk</th></tr></thead><tbody>${rows}</tbody></table>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

async function fetchAdminDashboard() {
    try {
        const data = await request('/api/admin/overview');
        const rows = (data.studentRecords || []).map(student => `
            <tr>
              <td>${student.fullName}</td>
              <td>${student.studentId}</td>
              <td>${student.department}</td>
              <td>${student.studentSuccessScore}</td>
            </tr>
        `).join('');

        document.getElementById('dashboardContent').innerHTML = `
          <div class="metric-grid">
            <div class="metric"><strong>${data.institutionalSummary.totalStudents}</strong><div>Total students</div></div>
            <div class="metric"><strong>${data.institutionalSummary.avgSuccessScore.toFixed(1)}</strong><div>Average score</div></div>
            <div class="metric"><strong>${data.institutionalSummary.pendingRegistrations}</strong><div>Pending registrations</div></div>
          </div>
          <h3 style="margin-top:24px;">All student records</h3>
          <table class="table"><thead><tr><th>Name</th><th>ID</th><th>Department</th><th>Success Score</th></tr></thead><tbody>${rows}</tbody></table>
        `;
    } catch (error) {
        setAlert(error.message, 'error');
    }
}

renderAuth();
