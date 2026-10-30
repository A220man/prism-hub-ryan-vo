import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { instancesApi } from '../api/instances';
import type { Instance, InstanceCreate, LaunchInfo } from '../types/api';

const InstancesPage: React.FC = () => {
  const [instances, setInstances] = useState<Instance[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showLaunchInfoModal, setShowLaunchInfoModal] = useState(false);
  const [launchInfo, setLaunchInfo] = useState<LaunchInfo | null>(null);
  const [launchInfoLoading, setLaunchInfoLoading] = useState(false);
  const [formData, setFormData] = useState<InstanceCreate>({
    name: '',
    version: '1.20.1',
    loader: '',
    loader_version: '',
    memory_min: 1024,
    memory_max: 4096,
  });
  const [submitting, setSubmitting] = useState(false);

  const navigate = useNavigate();

  const fetchInstances = async () => {
    try {
      setLoading(true);
      const response = await instancesApi.list();
      setInstances(response.data.instances);
      setError(null);
    } catch (err) {
      setError('Failed to load instances');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInstances();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await instancesApi.create(formData);
      setShowCreateModal(false);
      setFormData({ name: '', version: '1.20.1', loader: '', loader_version: '', memory_min: 1024, memory_max: 4096 });
      await fetchInstances();
    } catch (err) {
      setError('Failed to create instance');
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleLaunch = async (id: string) => {
    try {
      await instancesApi.launch(id);
      await fetchInstances();
    } catch (err) {
      setError('Failed to launch instance');
      console.error(err);
    }
  };

  const handleLaunchInfo = async (id: string) => {
    try {
      setLaunchInfoLoading(true);
      const response = await instancesApi.getLaunchInfo(id);
      setLaunchInfo(response.data);
      setShowLaunchInfoModal(true);
    } catch (err) {
      setError('Failed to load launch info');
      console.error(err);
    } finally {
      setLaunchInfoLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!window.confirm('Are you sure you want to delete this instance?')) return;
    try {
      await instancesApi.delete(id);
      await fetchInstances();
    } catch (err) {
      setError('Failed to delete instance');
      console.error(err);
    }
  };

  if (loading) {
    return <div className="loading">Loading instances...</div>;
  }

  return (
    <div className="instances-page">
      <header className="page-header">
        <h1>Instances</h1>
        <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
          New Instance
        </button>
      </header>

      {error && <div className="alert alert-error">{error}</div>}

      {instances.length === 0 ? (
        <div className="empty-state">
          <p>No instances yet. Create your first instance to get started.</p>
          <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
            Create Instance
          </button>
        </div>
      ) : (
        <div className="instances-grid">
          {instances.map((instance) => (
            <InstanceCard
              key={instance.id}
              instance={instance}
              onLaunch={handleLaunch}
              onDelete={handleDelete}
              onEdit={() => navigate(`/instances/${instance.id}/edit`)}
              onLaunchInfo={handleLaunchInfo}
            />
          ))}
        </div>
      )}

      {showCreateModal && (
        <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Create Instance</h2>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label htmlFor="name">Name *</label>
                <input
                  id="name"
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  maxLength={100}
                />
              </div>
              <div className="form-group">
                <label htmlFor="version">Version *</label>
                <input
                  id="version"
                  type="text"
                  value={formData.version}
                  onChange={(e) => setFormData({ ...formData, version: e.target.value })}
                  required
                  maxLength={50}
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="loader">Loader</label>
                  <input
                    id="loader"
                    type="text"
                    value={formData.loader}
                    onChange={(e) => setFormData({ ...formData, loader: e.target.value })}
                    placeholder="fabric, forge, etc."
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="loader_version">Loader Version</label>
                  <input
                    id="loader_version"
                    type="text"
                    value={formData.loader_version}
                    onChange={(e) => setFormData({ ...formData, loader_version: e.target.value })}
                  />
                </div>
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label htmlFor="memory_min">Min Memory (MB)</label>
                  <input
                    id="memory_min"
                    type="number"
                    value={formData.memory_min}
                    onChange={(e) => setFormData({ ...formData, memory_min: parseInt(e.target.value) })}
                    min={256}
                    max={16384}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="memory_max">Max Memory (MB)</label>
                  <input
                    id="memory_max"
                    type="number"
                    value={formData.memory_max}
                    onChange={(e) => setFormData({ ...formData, memory_max: parseInt(e.target.value) })}
                    min={512}
                    max={32768}
                  />
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={() => setShowCreateModal(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={submitting}>
                  {submitting ? 'Creating...' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {showLaunchInfoModal && launchInfo && (
        <div className="modal-overlay" onClick={() => setShowLaunchInfoModal(false)}>
          <div className="modal modal-large" onClick={(e) => e.stopPropagation()}>
            <h2>Launch Info: {launchInfo.instance.name}</h2>
            <div className="launch-info-content">
              <div className="info-section">
                <h3>Java Detection</h3>
                {launchInfo.java_detected ? (
                  <div className="java-detected">
                    <p><strong>Path:</strong> {launchInfo.java_detected.path}</p>
                    <p><strong>Version:</strong> {launchInfo.java_detected.version} (Major: {launchInfo.java_detected.major_version})</p>
                    <p><strong>Type:</strong> {launchInfo.java_detected.is_jdk ? 'JDK' : 'JRE'}</p>
                    <span className="badge badge-success">Suitable for Minecraft {launchInfo.instance.version}</span>
                  </div>
                ) : (
                  <div className="java-not-detected">
                    <p>No suitable Java installation found automatically.</p>
                    <p>Required: Java {launchInfo.required_java_version}+</p>
                    {launchInfo.java_executable && (
                      <p><strong>Using configured:</strong> {launchInfo.java_executable}</p>
                    )}
                    <span className="badge badge-warning">Manual configuration may be required</span>
                  </div>
                )}
              </div>

              <div className="info-section">
                <h3>Launch Command</h3>
                <pre className="launch-command">{launchInfo.launch_command.join(' ')}</pre>
                <button className="btn btn-secondary" onClick={() => navigator.clipboard.writeText(launchInfo.launch_command.join(' '))}>
                  Copy Command
                </button>
              </div>
            </div>
            <div className="modal-actions">
              <button className="btn btn-primary" onClick={() => setShowLaunchInfoModal(false)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const InstanceCard: React.FC<{
  instance: Instance;
  onLaunch: (id: string) => void;
  onDelete: (id: string) => void;
  onEdit: () => void;
  onLaunchInfo: (id: string) => void;
}> = ({ instance, onLaunch, onDelete, onEdit, onLaunchInfo }) => {
  const statusColors: Record<string, string> = {
    created: '#6c757d',
    downloading: '#ffc107',
    ready: '#28a745',
    launching: '#17a2b8',
    running: '#007bff',
    error: '#dc3545',
  };

  return (
    <div className="instance-card">
      <div className="instance-header">
        <h3>{instance.name}</h3>
        <span
          className="status-badge"
          style={{ backgroundColor: statusColors[instance.status] || '#6c757d' }}
        >
          {instance.status}
        </span>
      </div>
      <div className="instance-details">
        <p><strong>Version:</strong> {instance.version}</p>
        {instance.loader && <p><strong>Loader:</strong> {instance.loader} {instance.loader_version ? '@ ' + instance.loader_version : ''}</p>}
        <p><strong>Memory:</strong> {instance.memory_min}MB - {instance.memory_max}MB</p>
        <p><strong>Resolution:</strong> {instance.resolution_width}x{instance.resolution_height}</p>
      </div>
      <div className="instance-actions">
        <button
          className="btn btn-primary"
          onClick={() => onLaunch(instance.id)}
          disabled={instance.status === 'launching' || instance.status === 'running'}
        >
          {instance.status === 'launching' ? 'Launching...' : instance.status === 'running' ? 'Running' : 'Launch'}
        </button>
        <button className="btn btn-info" onClick={() => onLaunchInfo(instance.id)}>
          Launch Info
        </button>
        <button className="btn btn-secondary" onClick={onEdit}>
          Edit
        </button>
        <button className="btn btn-danger" onClick={() => onDelete(instance.id)}>
          Delete
        </button>
      </div>
    </div>
  );
};

export default InstancesPage;
