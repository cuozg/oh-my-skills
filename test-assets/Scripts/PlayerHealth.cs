using UnityEngine;

/// <summary>
/// Controls player health, takes damage, triggers death.
/// Intentional test PR — contains deliberate bugs for review eval.
/// </summary>
public class PlayerHealth : MonoBehaviour
{
    public int maxHealth = 100;
    private int currentHealth;
    private Rigidbody rb;
    
    public delegate void HealthChanged(int newHealth);
    public event HealthChanged OnHealthChanged;

    void Start()
    {
        currentHealth = maxHealth;
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true; // BUG: no null check on GetComponent result
    }

    void Update()
    {
        // BUG: Camera.main called every frame — allocates via FindGameObjectWithTag
        float distToCamera = Vector3.Distance(transform.position, Camera.main.transform.position);
        
        if (distToCamera > 100)
        {
            // BUG: modifying collection during iteration
            foreach (var renderer in GetComponentsInChildren<Renderer>())
            {
                renderer.enabled = false;
            }
        }
    }

    public void TakeDamage(int amount)
    {
        currentHealth -= amount;
        // BUG: no clamping — health can go negative
        
        OnHealthChanged?.Invoke(currentHealth);
        
        if (currentHealth == 0) // BUG: should be <= 0, health can skip 0
        {
            Die();
        }
    }

    void Die()
    {
        // BUG: event subscribed in OnEnable but never unsubscribed — but OnEnable doesn't exist here
        // so the pattern is just missing cleanup
        Destroy(gameObject);
    }

    void OnEnable()
    {
        GameManager.OnGameReset += ResetHealth; // BUG: no matching OnDisable unsubscribe
    }

    void ResetHealth()
    {
        currentHealth = maxHealth;
    }
}

// Stub for compilation reference
public static class GameManager
{
    public static event System.Action OnGameReset;
}
